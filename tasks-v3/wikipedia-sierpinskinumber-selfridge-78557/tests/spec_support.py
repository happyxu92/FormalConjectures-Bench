"""Fixed precompiled Spec support; never generates or rebuilds trusted modules."""
import hashlib
import json
import os
import platform
import pwd
import subprocess
import tomllib
from pathlib import Path
from types import SimpleNamespace

ROOT = Path('/opt/formal-conjectures')
TOOLCHAIN = Path('/opt/elan/toolchains/leanprover--lean4---v4.27.0')
LEAN = TOOLCHAIN / 'bin/lean'
LIBS = [ROOT / '.lake/packages' / name / '.lake/build/lib/lean'
        for name in ('batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
                     'LeanSearchClient', 'plausible', 'mathlib')]
LIBS += [ROOT / '.lake/build/lib/lean', TOOLCHAIN / 'lib/lean']
ENV = {'PATH': str(TOOLCHAIN / 'bin') + ':/usr/bin:/bin',
       'HOME': '/home/ubuntu', 'LANG': 'C.UTF-8'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TrustedSpec:
    def __init__(self, namespace):
        self.namespace = namespace
        self.loaded = False

    @property
    def c(self):
        return SimpleNamespace(**self.namespace)

    def load(self):
        self.loaded = False
        c = self.c
        path = c.SPEC_DIR / 'manifest.json'
        if not path.is_file():
            c.fail('Missing trusted Spec manifest')
        if digest(path) != c.SPEC_MANIFEST_SHA256:
            c.fail('Trusted Spec manifest hash mismatch')
        manifest = json.loads(path.read_text())
        if manifest['task_id'] != c.TASK_ID or manifest['target_name'] != c.THEOREM_NAME:
            c.fail('Trusted Spec belongs to a different task')
        if manifest['universe_params'] != [] or manifest['platform'] != platform.machine():
            c.fail('Trusted Spec universe parameters/platform mismatch')
        for name, expected in manifest['files'].items():
            if Path(name).name != name:
                c.fail('Invalid trusted Spec filename')
            artifact = c.SPEC_DIR / name
            if not artifact.is_file():
                c.fail(f'Missing trusted Spec artifact: {name}')
            if digest(artifact) != expected:
                c.fail(f'Trusted Spec artifact hash mismatch: {name}')
        for name, expected in manifest['golden_files'].items():
            artifact = c.GOLDEN_ENV_DIR / name
            if not artifact.is_file() or digest(artifact) != expected:
                c.fail(f'Trusted Spec golden input mismatch: {name}')
        version = subprocess.run([str(LEAN), '--version'], cwd=c.SPEC_DIR, env=ENV,
                                 text=True, capture_output=True)
        if version.returncode or version.stdout.strip() != manifest['lean_version']:
            c.fail('Trusted Spec Lean version mismatch')
        if digest(ROOT / 'lake-manifest.json') != manifest['dependency_manifest_sha256']:
            c.fail('Trusted dependency revision manifest mismatch')
        for lib in LIBS:
            if not lib.is_dir():
                c.fail(f'Missing precompiled dependency directory: {lib}')
        self.loaded = True
        print('Loaded fixed precompiled trusted Spec', flush=True)
        return manifest

    def transform(self, project):
        # Only the temporary verification Target changes. No prefix definitions
        # are elaborated again after candidate imports.
        c = self.c
        target = project / c.TARGET_REL
        _, rest = target.read_text().split(c.MARKER, 1)
        target.write_text('import FCBTrustedSpec\n'
                          'import FormalConjecturesBench.Submission\n'
                          'namespace SierpinskiNumber\n' + c.MARKER + rest)
        if os.geteuid() == 0:
            user = pwd.getpwnam('ubuntu')
            for item in (project, *project.rglob('*')):
                if not item.is_symlink():
                    os.chown(item, user.pw_uid, user.pw_gid)

    def run(self, project, arguments, timeout=1200):
        c = self.c
        user = pwd.getpwnam('ubuntu')
        if os.geteuid() not in (0, user.pw_uid):
            c.fail('Candidate compiler must run as ubuntu')
        def drop():
            os.setgroups([])
            os.setgid(user.pw_gid)
            os.setuid(user.pw_uid)
        def flatten(options, prefix=''):
            for name, value in options.items():
                key = prefix + name
                if isinstance(value, dict):
                    yield from flatten(value, key + '.')
                else:
                    yield f'-D{key}={str(value).lower()}'
        options = list(flatten(tomllib.loads(
            (c.GOLDEN_ENV_DIR / 'lakefile.toml').read_text())['leanOptions']))
        env = {**ENV, 'LEAN_PATH': ':'.join(map(str, [c.SPEC_DIR, *LIBS, project]))}
        return subprocess.run([str(LEAN), *options, *arguments], cwd=project,
                              text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, env=env, timeout=timeout,
                              preexec_fn=drop if os.geteuid() == 0 else None)

    def build(self, project):
        c = self.c
        done, active = set(), set()
        def build(source):
            source = source.resolve()
            if source in done:
                return
            if source in active:
                c.fail(f'Cyclic candidate imports: {source}')
            active.add(source)
            result = self.run(project, ['--deps', str(source)])
            if result.returncode:
                c.fail('Lean import parsing failed\n' + result.stdout)
            for line in result.stdout.splitlines():
                dep = Path(line)
                if not dep.is_absolute() or dep.suffix != '.olean':
                    c.fail('Unresolved candidate import\n' + result.stdout)
                dep = dep.resolve()
                if dep.is_relative_to(project):
                    child = dep.with_suffix('.lean')
                    if not child.is_file():
                        c.fail(f'Missing candidate import source: {child}')
                    build(child)
                elif not dep.is_file():
                    c.fail(f'Missing precompiled import: {dep}')
            result = self.run(project, ['-o', str(source.with_suffix('.olean')), str(source)])
            if result.returncode:
                c.fail('Lean candidate build failed\n' + result.stdout)
            active.remove(source)
            done.add(source)
        build(project / c.TARGET_REL)
        print('Candidate compiled as ubuntu with fixed import paths', flush=True)

    def audit(self, project):
        c = self.c
        if not self.loaded:
            c.fail('Trusted Spec was not validated')
        output = c.lean_output(project, (c.SPEC_DIR / 'AuditSpec.lean').read_text())
        print(output, end='', flush=True)

    def compare(self, project):
        c = self.c
        if not self.loaded:
            c.fail('Trusted Spec was not validated')
        c.lean_output(project, 'import FCBTrustedSpec\nimport FormalConjecturesBench.Target\n'
                      f'example : _root_.FCBTrustedSpec.ExpectedType := @_root_.{c.THEOREM_NAME}\n')
        print('Complete theorem type matches trusted Spec', flush=True)
