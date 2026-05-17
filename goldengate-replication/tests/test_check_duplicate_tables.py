import json
import subprocess
import sys

SCRIPT = 'goldengate-replication/scripts/check_duplicate_tables.py'

def run_script(base_path, mr_path):
    result = subprocess.run([
        sys.executable,
        SCRIPT,
        str(base_path),
        str(mr_path),
    ], capture_output=True, text=True)
    return result.returncode, result.stdout


def test_duplicate_detection(tmp_path):
    base = tmp_path / 'base.yaml'
    mr = tmp_path / 'mr.yaml'
    base.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1]')
    mr.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1]')
    rc, out = run_script(base, mr)
    assert rc == 2
    assert 'Duplicate tables found' in out


def test_warning_overlap(tmp_path):
    base = tmp_path / 'base.yaml'
    mr = tmp_path / 'mr.yaml'
    base.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1]')
    mr.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1, p2]')
    rc, out = run_script(base, mr)
    assert rc == 0
    assert 'partial pod overlap' in out
