import json
import subprocess
import sys

SCRIPT = 'goldengate-replication/scripts/validate_yaml_schema.py'

SCHEMA = {
    "type": "object",
    "properties": {
        "tables": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["schema", "name", "pods"],
                "properties": {
                    "schema": {"type": "string"},
                    "name": {"type": "string"},
                    "pods": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                    },
                },
                "additionalProperties": False,
            },
        }
    },
    "required": ["tables"],
    "additionalProperties": False,
}


def run_script(yaml_path, schema_path):
    result = subprocess.run(
        [sys.executable, SCRIPT, str(yaml_path), str(schema_path)],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def test_valid_yaml(tmp_path):
    yaml_file = tmp_path / 'tables.yaml'
    schema_file = tmp_path / 'schema.json'
    yaml_file.write_text('tables:\n  - schema: S\n    name: T\n    pods: [p1]')
    schema_file.write_text(json.dumps(SCHEMA))
    rc, _ = run_script(yaml_file, schema_file)
    assert rc == 0


def test_invalid_yaml(tmp_path):
    yaml_file = tmp_path / 'bad.yaml'
    schema_file = tmp_path / 'schema.json'
    yaml_file.write_text('tables:\n  - schema: S\n    name: T')
    schema_file.write_text(json.dumps(SCHEMA))
    rc, out = run_script(yaml_file, schema_file)
    assert rc == 2
    assert 'Schema validation error' in out
