#!/usr/bin/env python3
import sys
import yaml
from collections import defaultdict


def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def main():
    if len(sys.argv) != 3:
        print("Usage: check_duplicate_tables.py <base_yaml> <mr_yaml>")
        return 1
    base_path, mr_path = sys.argv[1:3]
    try:
        base_tables = load_yaml(base_path).get('tables', [])
        mr_tables = load_yaml(mr_path).get('tables', [])
        base_map = defaultdict(set)
        for t in base_tables:
            base_map[(t['schema'], t['name'])].update(t['pods'])

        duplicates = []
        warnings = []
        for t in mr_tables:
            key = (t['schema'], t['name'])
            new_pods = set(t['pods'])
            if key in base_map:
                if new_pods <= base_map[key]:
                    duplicates.append(key)
                elif new_pods & base_map[key]:
                    warnings.append(key)
        if duplicates:
            print("Duplicate tables found:")
            for d in duplicates:
                print(f"{d[0]}.{d[1]}")
            return 2
        if warnings:
            print("Warning: tables with partial pod overlap:")
            for w in warnings:
                print(f"{w[0]}.{w[1]}")
        return 0
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
