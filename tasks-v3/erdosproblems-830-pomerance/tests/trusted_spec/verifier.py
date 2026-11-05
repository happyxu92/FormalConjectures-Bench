"""Fixed-Spec verification support. No generation or runtime source fallback."""
import hashlib
import json
import os
import platform
import pwd
import shutil
import subprocess
import tempfile
import tomllib
from pathlib import Path


def install(ns):
    # A live view keeps the original checker's globals and test fixtures coherent.
    class Context:
        def __getattr__(self, name):
            return ns[name]
        def __setattr__(self, name, value):
            ns[name] = value
    c = Context()
    c.DEPENDENCY_ROOT = Path('/opt/formal-conjectures')
    c.TOOLCHAIN_ROOT = Path('/opt/elan/toolchains/leanprover--lean4---v4.27.0')
    c.LEAN = c.TOOLCHAIN_ROOT / 'bin/lean'
    c.DEPENDENCY_LIBS = [c.DEPENDENCY_ROOT / '.lake/packages' / name / '.lake/build/lib/lean'
        for name in ('batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
                     'LeanSearchClient', 'plausible', 'mathlib')]
    c.DEPENDENCY_LIBS += [c.DEPENDENCY_ROOT / '.lake/build/lib/lean', c.TOOLCHAIN_ROOT / 'lib/lean']
    c.ENV = {'PATH': str(c.TOOLCHAIN_ROOT / 'bin') + ':/usr/bin:/bin',
             'HOME': '/home/ubuntu', 'LANG': 'C.UTF-8'}
    c.SPEC_MANIFEST = None

    def sha256(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def load_trusted_spec():
        path = c.SPEC_DIR / 'manifest.json'
        if not path.is_file(): c.fail('Missing trusted Spec manifest')
        if sha256(path) != c.SPEC_MANIFEST_SHA256: c.fail('Trusted Spec manifest hash mismatch')
        m = json.loads(path.read_text())
        if m['task_id'] != c.TASK_ID or m['target_name'] != c.THEOREM_NAME:
            c.fail('Trusted Spec belongs to a different task')
        if m['universe_params'] != [] or m['platform'] != platform.machine():
            c.fail('Trusted Spec universe parameters/platform mismatch')
        for name, digest in m['files'].items():
            if Path(name).name != name: c.fail('Invalid trusted Spec filename')
            artifact = c.SPEC_DIR / name
            if not artifact.is_file(): c.fail(f'Missing trusted Spec artifact: {name}')
            if sha256(artifact) != digest: c.fail(f'Trusted Spec artifact hash mismatch: {name}')
        for name, digest in m['golden_files'].items():
            golden = c.GOLDEN_ENV_DIR / name
            if not golden.is_file() or sha256(golden) != digest:
                c.fail(f'Trusted Spec golden input mismatch: {name}')
        result = c.run([str(c.LEAN), '--version'], cwd=c.SPEC_DIR)
        if result.returncode or result.stdout.strip() != m['lean_version']:
            c.fail('Trusted Spec Lean version mismatch')
        if sha256(c.DEPENDENCY_ROOT / 'lake-manifest.json') != m['dependency_manifest_sha256']:
            c.fail('Trusted dependency revision manifest mismatch')
        for lib in c.DEPENDENCY_LIBS:
            if not lib.is_dir(): c.fail(f'Missing precompiled dependency directory: {lib}')
        c.SPEC_MANIFEST = m
        print('Loaded fixed precompiled trusted Spec', flush=True)
        return m

    def lean_env(project_dir):
        # Candidate paths and caches cannot precede Spec or its dependencies.
        return {**c.ENV, 'LEAN_PATH': ':'.join(map(str, [c.SPEC_DIR, *c.DEPENDENCY_LIBS, project_dir]))}

    def lean_options():
        def flatten(options, prefix=''):
            for name, value in options.items():
                if isinstance(value, dict): yield from flatten(value, prefix + name + '.')
                else: yield f'-D{prefix}{name}={str(value).lower()}'
        return list(flatten(tomllib.loads((c.GOLDEN_ENV_DIR / 'lakefile.toml').read_text())['leanOptions']))

    def run_lean(project_dir, arguments, timeout=1200):
        account = pwd.getpwnam('ubuntu')
        def drop_privileges():
            os.setgroups([])
            os.setgid(account.pw_gid)
            os.setuid(account.pw_uid)
        if os.geteuid() not in (0, account.pw_uid): c.fail('Candidate compiler must run as ubuntu')
        return subprocess.run([str(c.LEAN), *lean_options(), *arguments], cwd=project_dir,
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=lean_env(project_dir),
            timeout=timeout, preexec_fn=drop_privileges if os.geteuid() == 0 else None)

    def make_fresh_golden_project():
        tmp = tempfile.TemporaryDirectory(prefix='formal_conjectures_bench_')
        project = Path(tmp.name)
        shutil.copytree(c.GOLDEN_ENV_DIR, project, dirs_exist_ok=True)
        editable = project / c.EDITABLE_REL
        for rel, content in c.editable_lean_sources():
            dst = project / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(content, encoding='utf-8')
        target = project / c.TARGET_REL
        _, rest = target.read_text().split(c.MARKER, 1)
        target.write_text('import FCBTrustedSpec\nimport FormalConjecturesBench.Submission\n'
            'open scoped ArithmeticFunction.sigma\nopen Classical Filter Real\nnamespace Erdos830\n'
            + c.MARKER + rest, encoding='utf-8')
        if os.geteuid() == 0:
            account = pwd.getpwnam('ubuntu')
            for item in (project, *project.rglob('*')): os.chown(item, account.pw_uid, account.pw_gid)
        return tmp

    def check_build(project):
        done, active = set(), set()
        def build(source):
            source = source.resolve()
            if source in done: return
            if source in active: c.fail(f'Cyclic candidate imports: {source}')
            active.add(source)
            result = run_lean(project, ['--deps', str(source)])
            if result.returncode: c.fail('Lean import parsing failed\n' + result.stdout)
            for line in result.stdout.splitlines():
                dep = Path(line)
                if not dep.is_absolute() or dep.suffix != '.olean':
                    c.fail('Unresolved candidate import\n' + result.stdout)
                dep = dep.resolve()
                if dep.is_relative_to(project):
                    child = dep.with_suffix('.lean')
                    if not child.is_file(): c.fail(f'Missing candidate import source: {child}')
                    build(child)
                elif not dep.is_file(): c.fail(f'Missing precompiled import: {dep}')
            result = run_lean(project, ['-o', str(source.with_suffix('.olean')), str(source)])
            if result.returncode: c.fail('Lean candidate build failed\n' + result.stdout)
            active.remove(source)
            done.add(source)
        build(project / c.TARGET_REL)
        print('Candidate compiled as ubuntu with fixed import paths', flush=True)

    def lean_output(project, source):
        audit = project / '_formal_conjectures_bench_audit.lean'
        audit.write_text(source, encoding='utf-8')
        result = run_lean(project, [str(audit)], timeout=300)
        audit.unlink(missing_ok=True)
        if result.returncode: c.fail('Lean audit command failed\n' + result.stdout)
        return result.stdout

    def check_trusted_type(project):
        if c.SPEC_MANIFEST is None: c.fail('Trusted Spec was not validated')
        print(lean_output(project, (c.SPEC_DIR / 'AuditSpec.lean').read_text()), end='', flush=True)

    def check_golden_theorem_import(project):
        lean_output(project, 'import FCBTrustedSpec\nimport FormalConjecturesBench.Target\n'
            f'example : _root_.FCBTrustedSpec.ExpectedType := @_root_.{c.THEOREM_NAME}\n')
        print('Complete theorem type matches trusted Spec', flush=True)

    for fn in (load_trusted_spec, lean_env, lean_options, run_lean, make_fresh_golden_project,
               check_build, lean_output, check_trusted_type, check_golden_theorem_import):
        ns[fn.__name__] = fn
