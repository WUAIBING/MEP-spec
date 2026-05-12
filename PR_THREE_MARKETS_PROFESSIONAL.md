# PR Title
`feat(spec): add explicit three-market economics model to inter-bot spec and schema`

# PR Summary
This PR formalizes MEP's three-market economics model in the spec baseline.

It keeps `bounty_quanta` as non-negative integer economics and makes settlement direction explicit through:
- `economics.market`
- `economics.payment_direction`

# What Changed
- Updated `README.md` with explicit market field mapping
- Added `draft-mep-interbot-01.md` baseline spec
- Added `schemas/interbot-v1.schema.json` market consistency rules
- Added registries and changelog entries
- Added conformance vectors for valid/invalid three-market payloads
