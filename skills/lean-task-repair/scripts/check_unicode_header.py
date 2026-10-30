#!/usr/bin/env python3
"""Check one task's frozen headers and automatically repair surrogate pairs.

Exit codes: 0 = no issue or successfully repaired, 2 = unresolved/error.
Uses only the Python standard library. Never imports a checker or runs Lean.
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path


CHECKERS = (Path("tests/test_target.py"), Path("environment/data/checker/test_target.py"))
TARGET = Path("FormalConjecturesBench/Target.lean")
CONSTANTS = ("EXPECTED_HEADER", "MARKER", "EXPECTED_PREFIX_SHA256")


class HeaderError(ValueError):
    def __init__(self, case: str, message: str):
        super().__init__(message)
        self.case = case


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def scalar_header(header: str) -> str:
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in header):
        header = header.encode("utf-16-le", "surrogatepass").decode("utf-16-le")
    header.encode("utf-8")
    if not header.strip():
        raise ValueError("empty EXPECTED_HEADER")
    return header


def read_checker(data: bytes, path: Path) -> tuple[dict, dict, ast.Module]:
    tree = ast.parse(data.decode("utf-8"), filename=str(path))
    values, nodes = {}, {}
    # Include nested/chained assignments in duplicate detection; accept only a
    # single, simple module-level literal assignment for each required constant.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        names = [n.id for t in targets for n in ast.walk(t) if isinstance(n, ast.Name)]
        for name in set(names) & set(CONSTANTS):
            if name in values:
                raise ValueError(f"{path}: duplicate assignment: {name}")
            if node not in tree.body or len(targets) != 1 or not isinstance(targets[0], ast.Name):
                raise ValueError(f"{path}: require simple module-level assignment: {name}")
            value = ast.literal_eval(node.value)
            if not isinstance(value, str):
                raise ValueError(f"{path}: require string literal: {name}")
            values[name], nodes[name] = value, node.value
    for name in CONSTANTS:
        if name not in values:
            raise ValueError(f"{path}: missing constant: {name}")
    if not values["MARKER"]:
        raise ValueError(f"{path}: empty MARKER")
    return values, nodes, tree


def replace_header(data: bytes, node: ast.AST, replacement: bytes) -> bytes:
    # AST columns are UTF-8 byte offsets, not Python string indices.
    lines = data.splitlines(keepends=True)
    start = sum(map(len, lines[:node.lineno - 1])) + node.col_offset
    end = sum(map(len, lines[:node.end_lineno - 1])) + node.end_col_offset
    return data[:start] + replacement + data[end:]


def target_parts(text: str, values: dict, label: str) -> tuple[str, str, str]:
    marker = values["MARKER"]
    if text.count(marker) != 1:
        raise HeaderError("baseline_mismatch", f"{label}: require exactly one MARKER")
    prefix, rest = text.split(marker, 1)
    if digest(prefix.encode("utf-8")) != values["EXPECTED_PREFIX_SHA256"]:
        raise HeaderError("baseline_mismatch", f"{label}: frozen prefix SHA256 mismatch")
    header = values["EXPECTED_HEADER"].strip()
    after = rest.lstrip()
    if not after.startswith(header):
        raise HeaderError("baseline_mismatch", f"{label}: theorem header mismatch after Unicode repair")
    tail = after[len(header):].lstrip()
    if not tail.startswith(":=") or not tail[2:].strip():
        raise HeaderError("baseline_mismatch", f"{label}: missing := or empty proof")
    return prefix, header, tail[2:]


def checker_function(tree: ast.Module, values: dict):
    """Load only the two header-check functions, skipping all module-level code.

    These are trusted maintenance inputs, not sandboxed candidate code. Unknown
    helper dependencies fail explicitly rather than loading the whole checker.
    """
    functions = []
    for name in ("fail", "check_frozen_prefix_and_header"):
        matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
        if len(matches) != 1:
            raise ValueError(f"require exactly one function: {name}")
        fn = matches[0]
        if fn.decorator_list or fn.args.defaults or fn.args.kw_defaults:
            raise ValueError(f"unsupported decorated/default-argument function: {name}")
        functions.append(fn)
    module = ast.Module(body=functions, type_ignores=[])
    namespace = {**values, "hashlib": hashlib, "sys": sys}
    # Future annotations avoid evaluating checker-specific type names.
    import __future__
    exec(compile(module, "<checker-header-functions>", "exec",
                 flags=__future__.annotations.compiler_flag), namespace)
    return namespace["check_frozen_prefix_and_header"]


def invoke(fn, text: str) -> tuple[bool, str]:
    stderr = io.StringIO()
    with contextlib.redirect_stderr(stderr), contextlib.redirect_stdout(io.StringIO()):
        try:
            proof = fn(text)
        except SystemExit as exc:
            if exc.code != 1:
                raise ValueError(f"unexpected checker exit code: {exc.code}") from exc
            return False, stderr.getvalue()
    if not isinstance(proof, str) or not proof.strip():
        raise ValueError("checker returned an empty/non-string proof")
    return True, stderr.getvalue()


def verify_functions(tree: ast.Module, values: dict, targets: list[str]) -> None:
    fn = checker_function(tree, values)
    for text in targets:
        passed, error = invoke(fn, text)
        if not passed:
            raise ValueError(f"unchanged target rejected: {error.strip()}")
    prefix, header, proof = target_parts(targets[0], values, "mutation baseline")
    base = prefix + values["MARKER"] + "\n"
    # Change an operator/type token when present; otherwise change the name.
    if "=" in header:
        mutated = header.replace("=", "≠", 1)
    elif ":" in header:
        mutated = header.replace(":", ": ChangedType ", 1)
    else:
        mutated = "changed_" + header
    cases = (
        (base + mutated + " :=" + proof, "Target theorem header changed"),
        (base + header + " " + proof, "Target theorem no longer has a proof assignment"),
    )
    for changed, expected in cases:
        passed, error = invoke(fn, changed)
        if passed or expected not in error:
            raise ValueError(f"mutation not rejected for expected reason: {expected}; {error!r}")


def process(task: Path, report: dict) -> int:
    entries = []
    for rel in CHECKERS:
        path = task / rel
        data = path.read_bytes()
        try:
            values, nodes, tree = read_checker(data, path)
        except (ValueError, SyntaxError, TypeError) as exc:
            raise HeaderError("invalid_checker", f"{rel}: {exc}") from exc
        old = values["EXPECTED_HEADER"]
        has_unicode_issue = any(0xD800 <= ord(ch) <= 0xDFFF for ch in old)
        entry = {
            "path": str(rel), "sha256_before": digest(data),
            "header_before": old, "has_unicode_issue": has_unicode_issue,
            "modified": False, "verification": "not_run",
        }
        report["checkers"].append(entry)
        if has_unicode_issue:
            report["has_unicode_issue"] = True
        try:
            header = scalar_header(old)
        except UnicodeError as exc:
            entry["unicode_case"] = "isolated_surrogate"
            raise HeaderError("unrepairable_unicode", f"{rel}: isolated surrogate: {exc}") from exc
        except ValueError as exc:
            raise HeaderError("invalid_checker", f"{rel}: {exc}") from exc
        entry["unicode_case"] = "surrogate_pair" if has_unicode_issue else "none"
        entry["normalized_header"] = header
        corrected = {**values, "EXPECTED_HEADER": header}
        entries.append((path, data, corrected, nodes, tree, None))
    report["has_unicode_issue"] = any(e["has_unicode_issue"] for e in report["checkers"])
    for index, e in enumerate(entries):
        path, data, corrected, nodes, tree, _ = e
        rel = path.relative_to(task)
        entry = report["checkers"][index]
        targets = [task / "environment/data" / TARGET]
        targets.extend(task / p.parent / "golden_env" / TARGET for p in CHECKERS)
        texts = [p.read_text(encoding="utf-8") for p in targets]
        for p, text in zip(targets, texts):
            target_parts(text, corrected, str(p))
        values = {**corrected, "EXPECTED_HEADER": entry["header_before"]}
        try:
            verify_functions(tree, corrected, texts)
            passed, error = invoke(checker_function(tree, values), texts[0])
        except Exception as exc:
            entry["verification"] = "failed"
            raise HeaderError("verification_failed", f"{rel}: {exc}") from exc
        entry["normalized_header_checks"] = "passed"
        if not passed and (not entry["has_unicode_issue"] or "Target theorem header changed" not in error):
            entry["verification"] = "failed"
            raise HeaderError("verification_failed", f"{rel}: unexpected original checker failure: {error}")
        entry["original_header_passes"] = passed
        entries[index] = (path, data, corrected, nodes, tree, texts)

    first, second = entries
    if first[2] != second[2]:
        raise HeaderError("checker_mismatch", "checker constants disagree after surrogate normalization")
    masked = [replace_header(e[1], e[3]["EXPECTED_HEADER"], b"'<EXPECTED_HEADER>'") for e in entries]
    if masked[0] != masked[1]:
        raise HeaderError("checker_mismatch", "checker copies differ outside EXPECTED_HEADER; no files changed")
    needs_repair = report["has_unicode_issue"]
    report["copies_match_before"] = first[1] == second[1]
    if not needs_repair and not report["copies_match_before"]:
        raise HeaderError("checker_mismatch", "checker copies differ in literal formatting without a Unicode bug")
    report["trusted_inputs"] = [
        {"path": str(p.relative_to(task)), "sha256": digest(p.read_bytes())}
        for p in [task / "environment/data" / TARGET,
                  *(task / rel.parent / "golden_env" / TARGET for rel in CHECKERS)]
    ]
    if needs_repair:
        proposed = [replace_header(e[1], e[3]["EXPECTED_HEADER"],
                                   repr(e[2]["EXPECTED_HEADER"]).encode("utf-8")) for e in entries]
        if proposed[0] != proposed[1]:
            raise HeaderError("checker_mismatch", "proposed checker copies disagree")
        for e, data in zip(entries, proposed):
            values, _, tree = read_checker(data, e[0])
            verify_functions(tree, values, e[5])
            if e[0].read_bytes() != e[1]:
                raise HeaderError("input_changed", f"checker changed during preflight: {e[0]}")
        # Validate both in memory before any write; restore both on write/check failure.
        report.update(repair_attempted=True, repair_success=False)
        try:
            for e, data in zip(entries, proposed):
                e[0].write_bytes(data)
            for e, data in zip(entries, proposed):
                saved = e[0].read_bytes()
                if saved != data:
                    raise ValueError(f"unexpected bytes after write: {e[0]}")
                values, _, tree = read_checker(saved, e[0])
                verify_functions(tree, values, e[5])
        except BaseException as exc:
            rollback_errors = []
            for e in entries:
                try:
                    if e[0].read_bytes() != e[1]:
                        e[0].write_bytes(e[1])
                    if e[0].read_bytes() != e[1]:
                        raise OSError("restored bytes do not match original")
                except OSError as rollback_exc:
                    rollback_errors.append(f"{e[0]}: {rollback_exc}")
            report["rollback"] = "failed" if rollback_errors else "succeeded"
            if not isinstance(exc, Exception):
                raise
            if rollback_errors:
                raise HeaderError("rollback_failed", f"{exc}; rollback errors: {rollback_errors}") from exc
            raise HeaderError("repair_failed", f"repair failed; original files restored: {exc}") from exc
    report["copies_match_after"] = first[0].read_bytes() == second[0].read_bytes()
    for entry, e in zip(report["checkers"], entries):
        entry["verification"] = "passed"
    report.update(status="repaired" if needs_repair else "passed",
                  case="unicode_repaired" if needs_repair else "no_issue",
                  has_problem=bool(needs_repair),
                  repair_success=True if needs_repair else None,
                  verification="passed")
    return 0


def run_task(task: Path) -> tuple[int, dict]:
    task = task.resolve()
    report = {
        "task": str(task), "mode": "auto_repair", "status": "unresolved",
        "case": None, "has_problem": True, "has_unicode_issue": None,
        "repair_attempted": False, "repair_success": None, "modified": False,
        "rollback": "not_needed", "verification": "not_run", "checkers": [],
    }
    try:
        code = process(task, report)
    except Exception as exc:
        case = exc.case if isinstance(exc, HeaderError) else (
            "missing_file" if isinstance(exc, FileNotFoundError) else
            "io_error" if isinstance(exc, OSError) else "unexpected_error")
        report.update(case=case, error=str(exc))
        if report["repair_attempted"]:
            report["status"] = "failed"
        if case in {"verification_failed", "repair_failed", "rollback_failed"}:
            report["verification"] = "failed"
        code = 2
    # Report the actual final disk state, including after a failed repair/rollback.
    for entry in report["checkers"]:
        try:
            data = (task / entry["path"]).read_bytes()
            entry["sha256_after"] = digest(data)
            entry["modified"] = entry["sha256_before"] != entry["sha256_after"]
            values, _, _ = read_checker(data, task / entry["path"])
            entry["header_after"] = values["EXPECTED_HEADER"]
        except (OSError, ValueError, SyntaxError, TypeError) as exc:
            entry.update(modified=None, final_state_error=str(exc))
    changes = [e["modified"] for e in report["checkers"]]
    report["modified"] = True if any(changes) else None if None in changes else False
    report["unicode_issue_checker_count"] = sum(e["has_unicode_issue"] for e in report["checkers"])
    return code, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", type=Path, help="one task root, not a dataset directory")
    args = parser.parse_args()
    code, report = run_task(args.task)
    # ASCII JSON also safely records the original malformed surrogate strings.
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
