"""Regression tests for single-task Unicode header detection and repair."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).with_name("check_unicode_header.py")
spec = importlib.util.spec_from_file_location("check_unicode_header", SCRIPT)
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)

FUNCTIONS = '''
# This must never execute during header checks.
raise RuntimeError("checker module-level code executed")

def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)

def check_frozen_prefix_and_header(text: str) -> str:
    if MARKER not in text:
        fail("Target marker was removed")
    prefix, rest = text.split(MARKER, 1)
    if hashlib.sha256(prefix.encode("utf-8")).hexdigest() != EXPECTED_PREFIX_SHA256:
        fail("Code above the benchmark target marker changed")
    expected_header = EXPECTED_HEADER.strip()
    target_after_marker = rest.lstrip()
    if not target_after_marker.startswith(expected_header):
        fail("Target theorem header changed")
    after_header = target_after_marker[len(expected_header):].lstrip()
    if not after_header.startswith(":="):
        fail("Target theorem no longer has a proof assignment")
    return after_header[2:]
'''


class UnicodeHeaderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.task = Path(self.temp.name).resolve()
        self.header = 'theorem demo (x : Nat) : 𝓝 x = 𝓝 x\n  -- "quote" \\ path'
        self.prefix = "-- trusted prefix 𝓝\n"
        self.marker = "-- TARGET_BEGIN"
        self.paths = [self.task / rel for rel in repair.CHECKERS]
        self.make_task()

    def make_task(self, buggy=True, multiline=False):
        literal = json.dumps(self.header) if buggy else repr(self.header)
        assignment = f"EXPECTED_HEADER = {literal}  # retained comment\n"
        if multiline:
            assignment = f"π = 1; EXPECTED_HEADER = (\n    {literal}\n)  # retained comment\n"
        source = (f"MARKER = {self.marker!r}\n"
                  f"EXPECTED_PREFIX_SHA256 = {repair.digest(self.prefix.encode())!r}\n"
                  + assignment + FUNCTIONS)
        for path in self.paths:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding="utf-8")
        self.targets = [self.task / "environment/data" / repair.TARGET]
        self.targets.extend(p.parent / "golden_env" / repair.TARGET for p in self.paths)
        for path in self.targets:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.prefix + self.marker + "\n" + self.header + " := by\n  sorry\n",
                            encoding="utf-8")

    def run_repair(self):
        return repair.run_task(self.task)

    def assert_unresolved(self, case):
        code, report = self.run_repair()
        self.assertEqual(code, 2, report)
        self.assertEqual(report["case"], case, report)
        self.assertTrue(report["has_problem"])
        self.assertFalse(report["repair_attempted"])
        self.assertIsNone(report["repair_success"])
        self.assertFalse(report["modified"])
        return report

    def snapshot(self):
        return {p.relative_to(self.task): p.read_bytes() for p in self.task.rglob("*") if p.is_file()}

    def test_default_automatically_repairs_and_reports_case(self):
        code, report = self.run_repair()
        self.assertEqual(code, 0)
        self.assertEqual(report["case"], "unicode_repaired")
        self.assertTrue(report["has_problem"])
        self.assertTrue(report["has_unicode_issue"])
        self.assertTrue(report["repair_attempted"])
        self.assertTrue(report["repair_success"])
        self.assertTrue(report["modified"])
        self.assertEqual(report["unicode_issue_checker_count"], 2)
        self.assertEqual(report["verification"], "passed")
        self.assertTrue(all(e["has_unicode_issue"] for e in report["checkers"]))
        self.assertTrue(all(not e["original_header_passes"] for e in report["checkers"]))
        self.assertTrue(all(e["modified"] for e in report["checkers"]))
        self.assertTrue(all(e["header_after"] == self.header for e in report["checkers"]))

    def test_repair_both_and_repeat_without_changes(self):
        before = self.snapshot()
        code, report = self.run_repair()
        self.assertEqual((code, report["status"]), (0, "repaired"))
        self.assertTrue(report["copies_match_after"])
        for path in self.paths:
            values, _, _ = repair.read_checker(path.read_bytes(), path)
            self.assertEqual(values["EXPECTED_HEADER"], self.header)
            self.assertIn("# retained comment", path.read_text())
            self.assertEqual(before[path.relative_to(self.task)].replace(json.dumps(self.header).encode(),
                             repr(self.header).encode()), path.read_bytes())
        for path in self.targets:
            self.assertEqual(before[path.relative_to(self.task)], path.read_bytes())
        fixed = self.snapshot()
        self.assertEqual(self.run_repair()[1]["status"], "passed")
        self.assertEqual(fixed, self.snapshot())

    def test_one_bad_copy_is_repaired_and_synchronized(self):
        data = self.paths[1].read_bytes().replace(json.dumps(self.header).encode(), repr(self.header).encode())
        self.paths[1].write_bytes(data)
        code, report = self.run_repair()
        self.assertEqual((code, report["status"]), (0, "repaired"))
        self.assertEqual(report["unicode_issue_checker_count"], 1)
        self.assertEqual([e["modified"] for e in report["checkers"]], [True, False])
        self.assertEqual(self.paths[0].read_bytes(), self.paths[1].read_bytes())

    def test_multiline_literal_with_unicode_byte_offsets(self):
        self.make_task(multiline=True)
        self.assertEqual(self.run_repair()[0], 0)
        source = self.paths[0].read_text()
        self.assertIn("π = 1; EXPECTED_HEADER = ", source)
        self.assertIn("# retained comment", source)
        values, _, _ = repair.read_checker(self.paths[0].read_bytes(), self.paths[0])
        self.assertEqual(values["EXPECTED_HEADER"], self.header)

    def test_healthy_ascii_and_unicode_headers_unchanged(self):
        for header in ["theorem ascii (n : Nat) : n = n", self.header]:
            with self.subTest(header=header):
                self.header = header
                self.make_task(buggy=False)
                before = self.snapshot()
                code, report = self.run_repair()
                self.assertEqual((code, report["case"]), (0, "no_issue"))
                self.assertFalse(report["has_problem"])
                self.assertFalse(report["has_unicode_issue"])
                self.assertFalse(report["modified"])
                self.assertFalse(report["repair_attempted"])
                self.assertIsNone(report["repair_success"])
                self.assertEqual(before, self.snapshot())

    def test_lone_surrogates_rejected(self):
        for bad in ["\ud835", "\udcdd"]:
            with self.subTest(bad=repr(bad)):
                self.make_task()
                self.paths[1].write_bytes(self.paths[1].read_bytes().replace(
                    json.dumps(self.header).encode(), repr(bad).encode()))
                before = self.snapshot()
                report = self.assert_unresolved("unrepairable_unicode")
                self.assertTrue(report["has_unicode_issue"])
                self.assertEqual(report["checkers"][1]["unicode_case"], "isolated_surrogate")
                self.assertEqual(before, self.snapshot())

    def test_bad_trusted_inputs_cause_no_writes(self):
        for mutation in [lambda s: s.replace("theorem demo", "theorem changed"),
                         lambda s: s.replace("trusted prefix", "changed prefix"),
                         lambda s: s.replace(" := by", " by")]:
            with self.subTest(mutation=mutation):
                self.make_task()
                self.targets[-1].write_text(mutation(self.targets[-1].read_text()), encoding="utf-8")
                before = self.snapshot()
                self.assert_unresolved("baseline_mismatch")
                self.assertEqual(before, self.snapshot())

    def test_missing_duplicate_and_nonliteral_constants_rejected(self):
        for replacement in ["", "EXPECTED_HEADER = 'a'\nEXPECTED_HEADER = 'b'\n",
                            "EXPECTED_HEADER = 12\n", "EXPECTED_HEADER = str('x')\n"]:
            with self.subTest(replacement=replacement):
                self.make_task()
                data = self.paths[1].read_text().replace(
                    f"EXPECTED_HEADER = {json.dumps(self.header)}  # retained comment\n", replacement)
                self.paths[1].write_text(data)
                before = self.snapshot()
                self.assert_unresolved("invalid_checker")
                self.assertEqual(before, self.snapshot())

    def test_other_checker_differences_are_not_overwritten(self):
        self.paths[1].write_bytes(self.paths[1].read_bytes() + b"\n# different logic\n")
        before = self.snapshot()
        report = self.assert_unresolved("checker_mismatch")
        self.assertIn("outside EXPECTED_HEADER", report["error"])
        self.assertEqual(before, self.snapshot())

    def test_permissive_checker_fails_mutation_check(self):
        for path in self.paths:
            source = path.read_text().replace(
                "def check_frozen_prefix_and_header(text: str) -> str:\n",
                "def check_frozen_prefix_and_header(text: str) -> str:\n    return text\n")
            path.write_text(source)
        before = self.snapshot()
        report = self.assert_unresolved("verification_failed")
        self.assertIn("mutation not rejected", report["error"])
        self.assertEqual(before, self.snapshot())

    def test_write_failure_rolls_back_first_copy(self):
        before = self.snapshot()
        original = Path.write_bytes
        failed = False

        def fail_once(path, data):
            nonlocal failed
            if path == self.paths[1] and not failed:
                failed = True
                raise OSError("simulated second write failure")
            return original(path, data)

        with mock.patch.object(Path, "write_bytes", fail_once):
            code, report = self.run_repair()
        self.assertEqual(code, 2)
        self.assertEqual(report["case"], "repair_failed")
        self.assertTrue(report["repair_attempted"])
        self.assertFalse(report["repair_success"])
        self.assertEqual(report["rollback"], "succeeded")
        self.assertFalse(report["modified"])
        self.assertIn("simulated", report["error"])
        self.assertEqual(before, self.snapshot())

    def test_rollback_failure_reports_actual_remaining_change(self):
        original = Path.write_bytes
        first_writes = 0

        def fail_restore(path, data):
            nonlocal first_writes
            if path == self.paths[0]:
                first_writes += 1
                if first_writes == 2:
                    raise OSError("simulated rollback failure")
            if path == self.paths[1]:
                raise OSError("simulated second write failure")
            return original(path, data)

        with mock.patch.object(Path, "write_bytes", fail_restore):
            code, report = self.run_repair()
        self.assertEqual((code, report["case"]), (2, "rollback_failed"))
        self.assertEqual(report["rollback"], "failed")
        self.assertFalse(report["repair_success"])
        self.assertTrue(report["modified"])
        self.assertEqual([e["modified"] for e in report["checkers"]], [True, False])

    def test_missing_file_reports_unknown_unicode_state(self):
        self.paths[0].unlink()
        report = self.assert_unresolved("missing_file")
        self.assertIsNone(report["has_unicode_issue"])

    def test_cli_exit_codes_and_json_report(self):
        for code, case in [(0, "unicode_repaired"), (0, "no_issue")]:
            result = subprocess.run([sys.executable, str(SCRIPT), str(self.task)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, code, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["case"], case)
        self.paths[0].unlink()
        result = subprocess.run([sys.executable, str(SCRIPT), str(self.task)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
