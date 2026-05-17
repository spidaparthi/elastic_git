#!/usr/bin/env python3
import os
import sys
try:
    import cx_Oracle
except ImportError:
    cx_Oracle = None


ndefault_err = 1

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_table_exists.py <new_tables.txt>")
        return 1
    if cx_Oracle is None:
        print("cx_Oracle not installed")
        return 3
    file_path = sys.argv[1]
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")
    if not all([user, password, dsn]):
        print("Missing Oracle credentials")
        return 1
    try:
        conn = cx_Oracle.connect(user, password, dsn)
        cursor = conn.cursor()
        missing = []
        with open(file_path, 'r') as f:
            for line in f:
                schema, table = line.strip().split(',', 1)
                cursor.execute(
                    "select count(*) from dba_tables where owner = :1 and table_name = :2",
                    (schema.upper(), table.upper()),
                )
                count = cursor.fetchone()[0]
                if count == 0:
                    missing.append(f"{schema}.{table}")
        if missing:
            print("Missing tables:")
            for m in missing:
                print(m)
            return 2
        return 0
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 3
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    sys.exit(main())
