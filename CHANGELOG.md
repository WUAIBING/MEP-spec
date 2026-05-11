# MEP Specification Changelog

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
