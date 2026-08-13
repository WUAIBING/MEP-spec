import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CONFORMANCE_DIR = ROOT / "conformance"

SCHEMA_FIXTURES = (
    (
        ROOT / "schemas" / "interbot-v1.schema.json",
        "*.json",
        ("federation_*.json",),
    ),
    (
        ROOT / "schemas" / "federation-v1.schema.json",
        "federation_*.json",
        (),
    ),
)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    failures = []
    for schema_path, pattern, excluded_patterns in SCHEMA_FIXTURES:
        validator = Draft202012Validator(load_json(schema_path))
        for expectation in ("valid", "invalid"):
            paths = sorted((CONFORMANCE_DIR / expectation).glob(pattern))
            paths = [
                path for path in paths
                if not any(path.match(excluded) for excluded in excluded_patterns)
            ]
            for path in paths:
                errors = sorted(
                    validator.iter_errors(load_json(path)),
                    key=lambda err: list(err.path),
                )
                if expectation == "valid" and errors:
                    failures.append(
                        f"{path}: expected valid, got {errors[0].message}"
                    )
                if expectation == "invalid" and not errors:
                    failures.append(f"{path}: expected invalid, got valid")

    if failures:
        for failure in failures:
            print(failure)
        return 1

    print("schema conformance fixtures passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
