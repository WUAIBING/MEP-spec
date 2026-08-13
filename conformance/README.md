# MEP Conformance Vectors

This directory contains example payloads for schema and semantic checks.

The JSON files under `valid/` and `invalid/` are static schema fixtures.
Validators MUST NOT apply the runtime timestamp freshness rule to these
static fixtures. Freshness is a semantic/runtime check and should be tested
with generated timestamps.

## Valid

- `valid/minimal_compute.json`
- `valid/minimal_chat.json`
- `valid/minimal_result_response.json`
- `valid/minimal_error_response.json`
- `valid/minimal_data.json`
- `valid/string_ns.json`
- `valid/federation_profile.json`
- `valid/federation_invitation.json`
- `valid/federation_preview_grant.json`

## Invalid

- `invalid/float_bounty.json` (bounty must be integer)
- `invalid/market_mismatch.json` (market/direction mismatch)
- `invalid/missing_task.json` (request messages must carry instructions)
- `invalid/overflow_bounty.json` (bounty must fit u64)
- `invalid/federation_execution_enabled.json` (preview federation grants cannot execute work)

## Running Schema Fixtures

```bash
python -m pip install jsonschema
python conformance/validate_schema.py
```
