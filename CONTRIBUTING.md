# Contributing to MEP-spec

MEP-spec is the protocol specification repository for the Miao Exchange
Protocol. Contributions should improve the specification, schemas,
registries, conformance fixtures, or governance documents.

## Contribution Types

Use GitHub issues and pull requests for:

- Prose clarifications
- JSON Schema changes
- New conformance fixtures
- Intent type proposals
- Error code proposals
- Versioning or compatibility policy changes
- Implementation mapping notes from the MEP reference implementation

## Review Expectations

MEP is currently Draft. Breaking changes are allowed, but they should be
explicit and recorded in `CHANGELOG.md`.

Before opening a pull request:

1. Read `VERSIONING.md`.
2. Check whether your change is compatible or breaking.
3. Update `CHANGELOG.md` for normative behavior changes.
4. Add or update conformance fixtures when schema behavior changes.
5. Run:

```bash
python -m pip install jsonschema
python conformance/validate_schema.py
```

## Pull Request Guidelines

Pull requests should include:

- A short summary of the protocol behavior changed
- Files changed and why
- Whether the change is compatible or breaking
- Validation output, when applicable
- Links to related issues

Small editorial fixes may omit conformance output if no schema or
fixture behavior changed.

## Intent Type Proposals

Standard intent types are listed in `registry/intent-types.md`.

To propose a new standard intent type, open an issue with:

- Proposed intent type name
- Intended market: `compute`, `chat`, or `data`
- Message examples
- Settlement direction, if relevant
- Why private-use namespacing is not sufficient
- Whether at least one implementation already uses it

New intent types usually start as Proposed. They should become Standard
only after the meaning is clear and there is implementation interest.

## Private Intent Types

Private or experimental intent types do not need registry approval if
they use a dotted namespace, for example:

```text
com.example.custom.request
lab.routing.experiment
```

Private types MUST NOT use the `mep.` prefix unless they are defined by
this repository.

## Error Code Proposals

Standard error codes are listed in `registry/error-codes.md`.

To propose a new error code, open an issue with:

- Code name
- Retryable value
- Trigger condition
- Example message or validation failure
- Whether an existing code already covers the case

## Conformance Fixtures

Conformance fixtures live under `conformance/`.

- `conformance/valid/` contains payloads that MUST validate.
- `conformance/invalid/` contains payloads that MUST fail validation.
- Static fixtures MUST NOT be used for runtime timestamp freshness
  checks.

If a schema change accepts a new valid shape or rejects a previously
accepted invalid shape, add a fixture.

## Registry Maintenance

Registry files should include:

- Last updated date
- Status: Standard or Proposed
- Clear description
- Compatibility notes where useful

Git history is authoritative for exact authorship and change dates.
