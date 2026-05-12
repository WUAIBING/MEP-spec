import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "interbot-v1.schema.json"
CONFORMANCE_DIR = ROOT / "conformance"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures = []

    for path in sorted((CONFORMANCE_DIR / "valid").glob("*.json")):
        errors = sorted(validator.iter_errors(load_json(path)), key=lambda err: list(err.path))
        if errors:
            failures.append(f"{path}: expected valid, got {errors[0].message}")

    for path in sorted((CONFORMANCE_DIR / "invalid").glob("*.json")):
        errors = sorted(validator.iter_errors(load_json(path)), key=lambda err: list(err.path))
        if not errors:
            failures.append(f"{path}: expected invalid, got valid")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print("schema conformance fixtures passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
