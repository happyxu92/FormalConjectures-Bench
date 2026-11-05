"""Fixed precompiled Spec integration; no repair-time generation at verification."""
import types
from pathlib import Path

TASK_ID = "erdosproblems-647-twenty-four"
SPEC_MANIFEST_SHA256 = "22b103d156c7ef3e9d0d4a9bc02ae23d34c636d8b8800c78c85240b944a03715"


def install(g):
    root = Path('/opt/formal-conjectures')
    toolchain = Path('/opt/elan/toolchains/leanprover--lean4---v4.27.0')
    g.update({
        'SPEC_DIR': (g['TESTS_DIR'] / 'trusted_spec').resolve(),
        'SPEC_MANIFEST': None,
        'TASK_ID': TASK_ID,
        'SPEC_MANIFEST_SHA256': SPEC_MANIFEST_SHA256,
        'DEPENDENCY_ROOT': root,
        'DEPENDENCY_PACKAGES': root / '.lake/packages',
        'TOOLCHAIN_ROOT': toolchain,
        'LEAN': toolchain / 'bin/lean',
        'DEPENDENCY_LIBS': [root / '.lake/packages' / name / '.lake/build/lib/lean'
            for name in ('batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph',
                         'LeanSearchClient', 'plausible', 'mathlib')]
            + [root / '.lake/build/lib/lean', toolchain / 'lib/lean'],
        'ENV': {'PATH': str(toolchain / 'bin') + ':/usr/bin:/bin',
                'HOME': '/home/ubuntu', 'LANG': 'C.UTF-8'},
    })
    # Bind to the checker namespace: actual functions share the same validated
    # manifest, paths, original source checks, axiom audit, and canary.
    for f in (sha256, load_trusted_spec, lean_env, lean_options, run_lean,
              make_fresh_golden_project, check_build, lean_output,
              check_trusted_type, check_golden_theorem_import):
        g[f.__name__] = types.FunctionType(f.__code__, g, f.__name__, f.__defaults__)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_trusted_spec():
    global SPEC_MANIFEST
    import platform
    manifest_path = SPEC_DIR / 'manifest.json'
    if not manifest_path.is_file():
        fail('Missing trusted Spec manifest')
    if sha256(manifest_path) != SPEC_MANIFEST_SHA256:
        fail('Trusted Spec manifest hash mismatch')
    manifest = json.loads(manifest_path.read_text())
    if manifest['task_id'] != TASK_ID or manifest['target_name'] != THEOREM_NAME:
        fail('Trusted Spec belongs to a different task')
    if manifest['universe_params'] != [] or manifest['platform'] != platform.machine():
        fail('Trusted Spec universe parameters/platform mismatch')
    for name, digest in manifest['files'].items():
        if Path(name).name != name:
            fail('Invalid trusted Spec filename')
        path = SPEC_DIR / name
        if not path.is_file():
            fail(f'Missing trusted Spec artifact: {name}')
        if sha256(path) != digest:
            fail(f'Trusted Spec artifact hash mismatch: {name}')
    for name, digest in manifest['golden_files'].items():
        path = GOLDEN_ENV_DIR / name
        if not path.is_file() or sha256(path) != digest:
            fail(f'Trusted Spec golden input mismatch: {name}')
    version = run([str(LEAN), '--version'], cwd=SPEC_DIR)
    if version.returncode or version.stdout.strip() != manifest['lean_version']:
        fail('Trusted Spec Lean version mismatch')
    if sha256(DEPENDENCY_ROOT / 'lake-manifest.json') != manifest['dependency_manifest_sha256']:
        fail('Trusted dependency revision manifest mismatch')
    for lib in DEPENDENCY_LIBS:
        if not lib.is_dir():
            fail(f'Missing precompiled dependency directory: {lib}')
    SPEC_MANIFEST = manifest
    print('Loaded fixed precompiled trusted Spec', flush=True)
    return manifest


def lean_env(project_dir):
    return {**ENV, 'LEAN_PATH': ':'.join(map(str, [SPEC_DIR, *DEPENDENCY_LIBS, project_dir]))}


def lean_options():
    import tomllib
    def flatten(options, prefix=''):
        for name, value in options.items():
            key = prefix + name
            if isinstance(value, dict):
                yield from flatten(value, key + '.')
            else:
                yield f'-D{key}={str(value).lower()}'
    return list(flatten(tomllib.loads((GOLDEN_ENV_DIR / 'lakefile.toml').read_text())['leanOptions']))


def run_lean(project_dir, arguments, timeout=1200):
    import pwd
    account = pwd.getpwnam('ubuntu')
    def drop_privileges():
        os.setgroups([])
        os.setgid(account.pw_gid)
        os.setuid(account.pw_uid)
    if os.geteuid() not in (0, account.pw_uid):
        fail('Candidate compiler must run as ubuntu')
    return subprocess.run([str(LEAN), *lean_options(), *arguments], cwd=project_dir,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env=lean_env(project_dir), timeout=timeout,
        preexec_fn=drop_privileges if os.geteuid() == 0 else None)


def make_fresh_golden_project():
    tmp = tempfile.TemporaryDirectory(prefix='formal_conjectures_bench_')
    project_dir = Path(tmp.name)
    shutil.copytree(GOLDEN_ENV_DIR, project_dir, dirs_exist_ok=True)
    editable_src = TASK_DIR / EDITABLE_REL
    editable_dst = project_dir / EDITABLE_REL
    editable_dst.mkdir(parents=True, exist_ok=True)
    if editable_src.exists():
        for src in sorted(editable_src.rglob('*.lean')):
            if src.is_symlink() or not src.is_file():
                fail(f'Editable Lean source must be a regular file: {src.relative_to(TASK_DIR)}')
            dst = editable_dst / src.relative_to(editable_src)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    target = editable_dst / 'Target.lean'
    _, rest = target.read_text().split(MARKER, 1)
    target.write_text('import FCBTrustedSpec\nimport FormalConjecturesBench.Submission\n'
        'open Filter ArithmeticFunction.sigma\nnamespace Erdos647\n'
        + MARKER + rest, encoding='utf-8')
    if os.geteuid() == 0:
        import pwd
        account = pwd.getpwnam('ubuntu')
        for item in (project_dir, *project_dir.rglob('*')):
            os.chown(item, account.pw_uid, account.pw_gid)
    return tmp


def check_build(project_dir):
    done, active = set(), set()
    def build(source):
        source = source.resolve()
        if source in done:
            return
        if source in active:
            fail(f'Cyclic candidate imports: {source}')
        active.add(source)
        result = run_lean(project_dir, ['--deps', str(source)])
        if result.returncode:
            fail('Lean import parsing failed\n' + result.stdout)
        for line in result.stdout.splitlines():
            dep = Path(line)
            if not dep.is_absolute() or dep.suffix != '.olean':
                fail('Unresolved candidate import\n' + result.stdout)
            dep = dep.resolve()
            if dep.is_relative_to(project_dir):
                child = dep.with_suffix('.lean')
                if not child.is_file():
                    fail(f'Missing candidate import source: {child}')
                build(child)
            elif not dep.is_file():
                fail(f'Missing precompiled import: {dep}')
        result = run_lean(project_dir, ['-o', str(source.with_suffix('.olean')), str(source)])
        if result.returncode:
            fail('Lean candidate build failed\n' + result.stdout)
        active.remove(source)
        done.add(source)
    build(project_dir / TARGET_REL)
    print('Candidate compiled as ubuntu with fixed import paths', flush=True)


def lean_output(project_dir, source):
    tmp = project_dir / '_formal_conjectures_bench_audit.lean'
    tmp.write_text(source, encoding='utf-8')
    result = run_lean(project_dir, [str(tmp)], timeout=300)
    tmp.unlink(missing_ok=True)
    if result.returncode:
        fail('Lean audit command failed\n' + result.stdout)
    return result.stdout


def check_trusted_type(project_dir):
    if SPEC_MANIFEST is None:
        fail('Trusted Spec was not validated')
    print(lean_output(project_dir, (SPEC_DIR / 'AuditSpec.lean').read_text()), end='', flush=True)


def check_golden_theorem_import(project_dir):
    lean_output(project_dir, 'import FCBTrustedSpec\nimport FormalConjecturesBench.Target\n'
        f'example : _root_.FCBTrustedSpec.ExpectedType := @_root_.{THEOREM_NAME}\n')
    print('Complete theorem type matches trusted Spec', flush=True)
