"""Fixed Spec loading and isolated candidate compilation; no generation here."""
from pathlib import Path
import hashlib
import json
import os
import platform
import pwd
import shutil
import subprocess
import tempfile
import tomllib

TOOLCHAIN = Path('/opt/elan/toolchains/leanprover--lean4---v4.27.0')
LEAN = TOOLCHAIN / 'bin/lean'
ROOT = Path('/opt/formal-conjectures')
LIBS = [ROOT / '.lake/packages' / n / '.lake/build/lib/lean' for n in
        ('batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
         'LeanSearchClient', 'plausible', 'mathlib')] + [ROOT / '.lake/build/lib/lean', TOOLCHAIN / 'lib/lean']
ENV = {'PATH': str(TOOLCHAIN / 'bin') + ':/usr/bin:/bin',
       'HOME': '/home/ubuntu', 'LANG': 'C.UTF-8'}


def fail(message):
    import sys
    print(message, file=sys.stderr)
    raise SystemExit(1)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TrustedVerifier:
    def __init__(self, tests_dir, task_id, theorem_name, manifest_hash):
        self.spec_dir = (tests_dir / 'trusted_spec').resolve()
        self.golden_dir = tests_dir / 'golden_env'
        self.task_id = task_id
        self.theorem_name = theorem_name
        self.manifest_hash = manifest_hash
        self.manifest = None

    def load(self):
        path = self.spec_dir / 'manifest.json'
        if not path.is_file():
            fail('Missing trusted Spec manifest')
        if sha256(path) != self.manifest_hash:
            fail('Trusted Spec manifest hash mismatch')
        m = json.loads(path.read_text())
        if m['task_id'] != self.task_id or m['target_name'] != self.theorem_name:
            fail('Trusted Spec belongs to a different task')
        if m['universe_params'] != [] or m['platform'] != platform.machine():
            fail('Trusted Spec universe parameters/platform mismatch')
        for name, digest in m['files'].items():
            if Path(name).name != name:
                fail('Invalid trusted Spec filename')
            p = self.spec_dir / name
            if not p.is_file():
                fail('Missing trusted Spec artifact: ' + name)
            if sha256(p) != digest:
                fail('Trusted Spec artifact hash mismatch: ' + name)
        for name, digest in m['golden_files'].items():
            p = self.golden_dir / name
            if not p.is_file() or sha256(p) != digest:
                fail('Trusted Spec golden input mismatch: ' + name)
        v = subprocess.run([str(LEAN), '--version'], cwd=self.spec_dir,
                           env=ENV, capture_output=True, text=True)
        if v.returncode or v.stdout.strip() != m['lean_version']:
            fail('Trusted Spec Lean version mismatch')
        if sha256(ROOT / 'lake-manifest.json') != m['dependency_manifest_sha256']:
            fail('Trusted dependency revision manifest mismatch')
        for lib in LIBS:
            if not lib.is_dir():
                fail('Missing precompiled dependency directory: ' + str(lib))
        self.manifest = m
        print('Loaded fixed precompiled trusted Spec', flush=True)
        return m

    def run_lean(self, project, arguments, timeout=1200):
        if self.manifest is None:
            fail('Trusted Spec was not validated')
        def flatten(options, prefix=''):
            for k, v in options.items():
                if isinstance(v, dict):
                    yield from flatten(v, prefix + k + '.')
                else:
                    yield '-D' + prefix + k + '=' + str(v).lower()
        options = list(flatten(tomllib.loads((self.golden_dir / 'lakefile.toml').read_text())['leanOptions']))
        account = pwd.getpwnam('ubuntu')
        def drop():
            os.setgroups([])
            os.setgid(account.pw_gid)
            os.setuid(account.pw_uid)
        if os.geteuid() not in (0, account.pw_uid):
            fail('Candidate compiler must run as ubuntu')
        env = {**ENV, 'LEAN_PATH': ':'.join(map(str, [self.spec_dir, *LIBS, project]))}
        return subprocess.run([str(LEAN), *options, *arguments], cwd=project,
                              env=env, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, timeout=timeout,
                              preexec_fn=drop if os.geteuid() == 0 else None)

    def make_project(self, task_dir):
        if self.manifest is None:
            fail('Trusted Spec was not validated')
        tmp = tempfile.TemporaryDirectory(prefix='formal_conjectures_bench_')
        project = Path(tmp.name)
        shutil.copytree(self.golden_dir, project, dirs_exist_ok=True)
        for src in sorted((task_dir / 'FormalConjecturesBench').rglob('*.lean')):
            if src.is_symlink() or not src.is_file():
                fail('Editable Lean source must be a regular file: ' + str(src))
            dst = project / src.relative_to(task_dir)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        target = project / 'FormalConjecturesBench/Target.lean'
        marker = '-- FORMAL_CONJECTURES_BENCH_TARGET_BEGIN'
        _, rest = target.read_text().split(marker, 1)
        target.write_text('import FCBTrustedSpec\nimport FormalConjecturesBench.Submission\n'
                          'namespace OeisA358684\nopen Nat\n' + marker + rest)
        if os.geteuid() == 0:
            account = pwd.getpwnam('ubuntu')
            for item in (project, *project.rglob('*')):
                os.chown(item, account.pw_uid, account.pw_gid)
        return tmp

    def build(self, project):
        done, active = set(), set()
        def build(source):
            source = source.resolve()
            if source in done:
                return
            if source in active:
                fail('Cyclic candidate imports: ' + str(source))
            active.add(source)
            result = self.run_lean(project, ['--deps', str(source)])
            if result.returncode:
                fail('Lean import parsing failed\n' + result.stdout)
            for line in result.stdout.splitlines():
                dep = Path(line)
                if not dep.is_absolute() or dep.suffix != '.olean':
                    fail('Unresolved candidate import\n' + result.stdout)
                dep = dep.resolve()
                if dep.is_relative_to(project):
                    child = dep.with_suffix('.lean')
                    if not child.is_file():
                        fail('Missing candidate import source: ' + str(child))
                    build(child)
                elif not dep.is_file():
                    fail('Missing precompiled import: ' + str(dep))
            result = self.run_lean(project, ['-o', str(source.with_suffix('.olean')), str(source)])
            if result.returncode:
                fail('Lean candidate build failed\n' + result.stdout)
            active.remove(source)
            done.add(source)
        build(project / 'FormalConjecturesBench/Target.lean')
        print('Candidate compiled as ubuntu with fixed import paths', flush=True)

    def output(self, project, source):
        p = project / '_formal_conjectures_bench_audit.lean'
        p.write_text(source)
        result = self.run_lean(project, [str(p)], timeout=300)
        p.unlink(missing_ok=True)
        if result.returncode:
            fail('Lean audit command failed\n' + result.stdout)
        return result.stdout

    def audit(self, project):
        print(self.output(project, (self.spec_dir / 'AuditSpec.lean').read_text()), end='', flush=True)

    def compare(self, project):
        self.output(project, 'import FCBTrustedSpec\nimport FormalConjecturesBench.Target\n'
                    + 'example : _root_.FCBTrustedSpec.ExpectedType := @_root_.' + self.theorem_name + '\n')
        print('Complete theorem type matches trusted Spec', flush=True)
