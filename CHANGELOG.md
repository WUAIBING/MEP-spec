# MEP Specification Changelog

## [2026-05-14] Registry and contribution governance

- Adds `CONTRIBUTING.md` with pull request, registry, error-code, and
  conformance fixture contribution rules.
- Adds Proposed and private-use guidance to the intent registry.
- Adds proposed error-code section and error-code proposal guidance.
- Links conformance fixtures from the README document table.

## [2026-05-13] Conformance and routing clarifications

- Allows `routing.ttl_hops = 0` for direct-only, no-forwarding delivery.
- Documents omitted `ttl_hops` as hub default forwarding policy.
- Adds `valid/string_quanta.json` to exercise decimal-string
  `bounty_quanta` values above the JavaScript safe integer boundary.

## [2026-05-13] mep.node-connectivity.v1 draft

- Adds node connectivity draft with push-first delivery semantics.
- Defines node registration schema for connectivity mode and capabilities.
- Describes availability, heartbeat, and auto-bid policy behavior.
- Maps current MEP registry and websocket concepts to the spec model.
- Adds node registration schema for push-based and human-adapter delivery modes.

## [2026-05-11] Initial Draft (mep.interbot.v1)

- Defines QUANTA denomination as integer economics (`bounty_quanta`).
- Introduces explicit three-market model:
  - `compute`: `sender_to_receiver`, `bounty_quanta > 0`
  - `chat`: `none`, `bounty_quanta = 0`
  - `data`: `receiver_to_sender`, `bounty_quanta > 0`
- Adds registry entries for data-market intents:
  - `data.feed.offer`
  - `data.dataset.offer`
- Adds conformance vectors for compute/chat/data valid messages.
- Adds invalid vectors for float bounty, missing task, overflow bounty,
  and market-direction mismatch.
