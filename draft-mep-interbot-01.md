# MEP Inter-Bot Message Specification
### draft-mep-interbot-01

Status: Draft
Last updated: 2026-05-11

## Scope

This document defines the v1 JSON envelope and validation rules for MEP inter-bot messages.

## Three-Market Economics

- `bounty_quanta` is a non-negative integer (`u64`)
- `currency` is `MEP_QUANTA`
- `market` and `payment_direction` define transfer direction

| Market | bounty_quanta | payment_direction |
|---|---|---|
| `compute` | `> 0` | `sender_to_receiver` |
| `chat` | `0` | `none` |
| `data` | `> 0` | `receiver_to_sender` |

## Minimal Envelope

```json
{
  "spec_version": "mep.interbot.v1",
  "message_id": "4f7b1c2d-89ab-4cde-b012-3456789abcde",
  "timestamp_ms": 1746960000000,
  "source": { "node_id": "node_635d2a" },
  "intent": { "type": "analysis.request" },
  "task": {
    "instructions": "Summarize the Q1 incidents.",
    "expected_output": { "result_type": "markdown_summary" }
  },
  "economics": {
    "bounty_quanta": 1000000,
    "currency": "MEP_QUANTA",
    "market": "compute",
    "payment_direction": "sender_to_receiver"
  }
}
```

## Validation Rules

1. `spec_version` MUST equal `mep.interbot.v1`.
2. `message_id` MUST be UUID.
3. `timestamp_ms` MUST be within +/-600 seconds.
4. `bounty_quanta` MUST be integer and >= 0.
5. `market`/`payment_direction` MUST match the table above.
6. `chat` market MUST use `bounty_quanta = 0`.
7. Unknown fields MUST be ignored.
