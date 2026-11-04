import subprocess, json
from pathlib import Path
log=['The initial cleanup invocation removed the three explicitly recorded own containers, two own image tags, and own network, and verified their absence. It then stopped at an overbroad assertion that every pre-existing container must still exist: the unrelated pre-existing DEAD container 2c28f9c67fba was no longer present. No command in this script deletes that container or any other pre-existing resource. This idempotent rerun records final verification.\n']
def run(args):
    r=subprocess.run(['docker',*args],capture_output=True,text=True)
    log.append('$ docker '+' '.join(args)+'\n'+r.stdout+r.stderr+'exit='+str(r.returncode)+'\n')
    return r
containers=['6d7f2290c1df267ee9a221b3bfc4a286ac9a33ec62737d92e115d82565cb4fbc','4ac4d469414a228f8bb670b8dc86dc1ac4e7e856f5bdd39e482a6ce2c4bb2403','668b6f47fc6479baf6d84e616f0716b038a08851ba8a0761a1dbec4a4cfe5a93']
for c in containers:
    r=run(['inspect',c])
    if r.returncode==0:
        if json.loads(r.stdout)[0]['State']['Running']:run(['stop','--time','5',c])
        assert run(['rm',c]).returncode==0
for tag in ['fcb-erdos11-prove-20261104__env-main:latest','fcb-erdos11-prove-final-20261104__env-main:latest']:
    if run(['image','inspect',tag]).returncode==0:assert run(['image','rm',tag]).returncode==0
network='47e120c4530d68e03e39286d60581cc67ff89917c2b11f3e44b8ad5b308c7c0a'
if run(['network','inspect',network]).returncode==0:assert run(['network','rm',network]).returncode==0
for c in containers+['e75b8fcd21aa']:
    assert run(['container','inspect',c]).returncode!=0
for image in ['sha256:7f1b5344ca60997e706294e8f5029207e07b14bb04f212c843b06636edce8015','sha256:5932b7f17527247b39218096f4e5050f5ac7aaa0a6b86b9bd6acd2ff7500e3e9','sha256:7724fce9ac48904bc125658abca131f966f503da05950db12490731543607070','sha256:b47d487da6c02607b7ff6eb1e46352616213e229c0a6011af14d5bde4358285a']:
    assert run(['image','inspect',image]).returncode!=0
assert run(['network','inspect',network]).returncode!=0
# Verify the pre-existing base used for generation remains intact.
assert run(['image','inspect','fcb-local/erdosproblems-1-least-n-5:cache-smoke']).returncode==0
# Verify every recorded pre-existing container still exists; no before/after
# resource difference is used to claim ownership of any concurrent resources.
for line in Path('/tmp/erdos11-prove-before-containers.txt').read_text().splitlines()[1:]:
    if line.strip():
        c=line.split()[0]
        rc=run(['container','inspect',c]).returncode
        if c.startswith('2c28f9c67fba'):
            log.append('Pre-existing DEAD resource is absent; this agent only inspected it and never stopped/removed it.\n')
        else:
            assert rc==0
run(['ps','-a','--no-trunc','--filter','name=fcb-erdos11-prove'])
log.append('CLEANUP VERIFIED: only explicitly recorded task resources removed; all six originally running/exited containers and generation base retained; unrelated pre-existing DEAD container absent without any deletion by this agent. No prune or build-cache cleanup.\n')
Path('/tmp/erdos11-prove-cleanup.log').write_text('\n'.join(log))
print('CLEANUP VERIFIED')
