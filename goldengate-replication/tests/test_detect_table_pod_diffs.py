import subprocess
import sys

SCRIPT = 'goldengate-replication/scripts/detect_table_pod_diffs.py'

def run_script(base_path, mr_path, output_path):
    result = subprocess.run([
        sys.executable,
        SCRIPT,
        str(base_path),
        str(mr_path),
        str(output_path),
    ], capture_output=True, text=True)
    return result.returncode


def test_detect_diffs(tmp_path):
    base = tmp_path / 'base.yaml'
    mr = tmp_path / 'mr.yaml'
    out_file = tmp_path / 'new.txt'
    base.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1]')
    mr.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1, p2]\n  - schema: S\n    name: U\n    pods: [p2]')
    rc = run_script(base, mr, out_file)
    assert rc == 0
    lines = out_file.read_text().splitlines()
    assert sorted(lines) == ['S,T', 'S,U']
