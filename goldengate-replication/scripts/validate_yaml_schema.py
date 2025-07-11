#!/usr/bin/env python3
import json
import sys
import yaml
from jsonschema import validate, ValidationError


def main():
    if len(sys.argv) != 3:
        print("Usage: validate_yaml_schema.py <yaml_file> <schema_file>")
        return 1
    yaml_file, schema_file = sys.argv[1:3]
    try:
        with open(yaml_file, 'r') as yf:
            data = yaml.safe_load(yf) or {}
        with open(schema_file, 'r') as sf:
            schema = json.load(sf)
        validate(instance=data, schema=schema)
    except FileNotFoundError as exc:
        print(f"File not found: {exc}")
        return 1
    except ValidationError as exc:
        print(f"Schema validation error: {exc.message}")
        return 2
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
