#!/usr/bin/env python3
import sys
import yaml


def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def main():
    if len(sys.argv) != 4:
        print("Usage: detect_table_pod_diffs.py <base_yaml> <mr_yaml> <output>")
        return 1
    base_path, mr_path, output_path = sys.argv[1:4]
    try:
        base = load_yaml(base_path).get('tables', [])
        mr = load_yaml(mr_path).get('tables', [])

        base_set = set((t['schema'], t['name'], pod) for t in base for pod in t.get('pods', []))
        unique_new = set()
        for t in mr:
            for pod in t.get('pods', []):
                entry = (t['schema'], t['name'], pod)
                if entry not in base_set:
                    unique_new.add((t['schema'], t['name']))

        with open(output_path, 'w') as out:
            for schema, name in sorted(unique_new):
                out.write(f"{schema},{name}\n")
        return 0
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
