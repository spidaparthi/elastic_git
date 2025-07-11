#!/usr/bin/env python3
"""Validate new Goldengate table definitions."""

import os
import sys
import yaml
import subprocess
from typing import List

REQUIRED_KEYS = {"schema", "table", "dbs"}
STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "state", "replicated_tables.yaml")


def load_existing_tables() -> List[str]:
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("existing", [])


def lint_yaml(path: str) -> None:
    """Run yamllint on the given file."""
    print(f"Linting {path}")
    subprocess.run(["yamllint", path], check=True)


def validate_schema(doc: dict) -> None:
    missing = REQUIRED_KEYS - doc.keys()
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")
    if not isinstance(doc["dbs"], list):
        raise ValueError("'dbs' must be a list")


def table_exists_in_db(conn_str: str, schema: str, table: str) -> None:
    """Verify the table exists in the database."""
    try:
        import cx_Oracle
    except Exception as exc:  # pragma: no cover - optional dependency
        print(f"Skipping DB check: {exc}")
        return
    query = f"SELECT 1 FROM {schema}.{table} WHERE 1=0"
    with cx_Oracle.connect(conn_str) as conn:
        cur = conn.cursor()
        cur.execute(query)


def main(path: str) -> None:
    errors = []
    existing = load_existing_tables()
    conn_str = os.environ.get("DB_CONN_STRING")
    pending = []
    for fname in os.listdir(path):
        if not fname.endswith(".yaml"):
            continue
        fpath = os.path.join(path, fname)
        try:
            lint_yaml(fpath)
            with open(fpath, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            validate_schema(data)
            table_name = f"{data['schema']}.{data['table']}"
            if table_name in existing:
                raise ValueError(f"Table {table_name} already replicated")
            if conn_str:
                table_exists_in_db(conn_str, data["schema"], data["table"])
            pending.append(table_name)
            print(f"Validated {table_name}")
        except Exception as exc:  # pragma: no cover - simple error capture
            errors.append(f"{fname}: {exc}")
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    pending_file = os.path.join(os.path.dirname(__file__), "..", "state", "pending_tables.txt")
    with open(pending_file, "w", encoding="utf-8") as fh:
        for tbl in pending:
            fh.write(f"{tbl}\n")
    print(f"Wrote {len(pending)} pending tables to {pending_file}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "tables")
    main(path)
