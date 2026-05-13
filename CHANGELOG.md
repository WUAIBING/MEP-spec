# MEP Specification Changelog

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
  - `data.label.request`
- Adds conformance vectors for compute/chat/data valid messages.
- Adds invalid vectors for float bounty and market-direction mismatch.
