import subprocess
import sys
from pathlib import Path

SCRIPT = 'goldengate-replication/scripts/validate_table_exists.py'

def test_missing_cx_oracle(tmp_path):
    new_tables = tmp_path / 'new_tables.txt'
    new_tables.write_text('S,T\n')
    result = subprocess.run([sys.executable, SCRIPT, str(new_tables)], capture_output=True, text=True)
    assert result.returncode == 3
    assert 'cx_Oracle not installed' in result.stdout
