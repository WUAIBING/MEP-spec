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

## Invalid

- `invalid/float_quanta.json` (bounty must be integer)
- `invalid/market_mismatch.json` (market/direction mismatch)
- `invalid/missing_task.json` (request messages must carry instructions)
- `invalid/overflow_quanta.json` (bounty must fit u64)

## Running Schema Fixtures

```bash
python -m pip install jsonschema
python conformance/validate_schema.py
```
