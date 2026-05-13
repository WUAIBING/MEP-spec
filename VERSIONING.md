# MEP Specification Versioning Policy

## Version Identifiers

MEP specification identifiers use this form:

```text
mep.<spec-name>.v<major>
```

Current identifiers:

| Identifier | Document | Status |
|---|---|---|
| `mep.interbot.v1` | `draft-mep-interbot-01.md` | Draft |
| `mep.node-connectivity.v1` | `draft-mep-node-connectivity-01.md` | Draft |

The identifier appears in protocol payloads as `spec_version` where
applicable. For `mep.interbot.v1`, request messages MUST use:

```json
"spec_version": "mep.interbot.v1"
```

## Stability Levels

| Level | Meaning |
|---|---|
| Draft | May change. Implementers should expect revisions. |
| Candidate | Feature-complete enough for independent implementation. Breaking changes require explicit justification. |
| Stable | Production-stable. Breaking changes require a new major version. |

The current repository state is Draft.

## Compatibility Rules

### Backward-compatible changes

The following changes may be made within the same major version:

- Adding optional fields
- Adding registered intent types
- Adding registered error codes
- Clarifying prose without changing behavior
- Adding conformance fixtures
- Tightening non-normative examples

### Breaking changes

The following changes require a new major version once a spec reaches
Candidate or Stable:

- Removing a required field
- Renaming a required field
- Changing the type or denomination of `bounty_quanta`
- Changing market/payment-direction semantics
- Changing unknown-field handling
- Rejecting messages that were previously valid under the same major version
- Removing a standard intent type without a deprecation path

While the spec is Draft, breaking changes are allowed but SHOULD be
recorded in `CHANGELOG.md`.

## Unknown Field Rule

Receivers MUST ignore unknown fields unless the active specification
explicitly says the field changes validation. This rule is the primary
mechanism for compatible evolution.

## Extension Policy

Private or experimental intent types MUST use a dotted namespace, such
as:

```text
com.example.custom.request
lab.routing.experiment
```

Standard intent types are maintained in `registry/intent-types.md`.

## Deprecation Policy

Draft specs MAY rename or remove fields when necessary, but the
changelog SHOULD record the reason. Candidate and Stable specs SHOULD
mark fields deprecated before removal and SHOULD keep deprecated fields
valid until the next major version.

## Design Decisions Preserved in v1 Draft

These decisions are part of the v1 direction and SHOULD NOT change
without explicit review:

- `bounty_quanta` is integer QUANTA, not floating-point SECONDS.
- 1 QUANTA = 10^-9 SECONDS.
- Data-market direction is represented by `payment_direction`, not by a
  negative numeric bounty.
- Unknown fields are ignored for forward compatibility.
- Node connectivity is push-first; polling is fallback behavior.
