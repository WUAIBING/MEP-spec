# MEP Error Code Registry

Last updated: 2026-05-14

Error codes are stable identifiers for validation and runtime failures.
Use registered codes when possible. Private implementations MAY use
namespaced codes such as `COM_EXAMPLE_POLICY_REJECTED`, but standard
codes should be proposed through `CONTRIBUTING.md`.

| Code | Retryable | Description |
|---|---|---|
| `VERSION_NOT_SUPPORTED` | false | `spec_version` is not recognized |
| `TIMESTAMP_OUT_OF_RANGE` | false | `timestamp_ms` outside allowed skew window |
| `INVALID_MESSAGE_ID` | false | `message_id` format is invalid |
| `INTENT_TYPE_UNKNOWN` | false | `intent.type` not registered and not valid private format |
| `PAYLOAD_TOO_LARGE` | false | `task.instructions` exceeds max size |
| `TTL_EXCEEDED` | false | `routing.ttl_hops` reached forwarding limit |
| `INVALID_ECONOMICS` | false | Invalid market/direction/bounty combination |
| `INSUFFICIENT_FUNDS` | false | Required payer has insufficient balance |
| `DUPLICATE_MESSAGE` | false | `message_id` already processed |
| `NODE_NOT_FOUND` | false | Target node is not registered |
| `HITL_TIMEOUT` | false | Human decision timeout exceeded |
| `HITL_REJECTED` | false | Human decision rejected task |
| `HUB_UNAVAILABLE` | true | Hub temporarily unavailable |
| `RATE_LIMITED` | true | Sender exceeded request rate |

## Proposed Codes

| Code | Retryable | Description |
|---|---|---|
| `RESPONSE_CONFLICT` | false | Response contains both `result` and `error`, or neither |
| `WEBHOOK_DELIVERY_FAILED` | true | Hub could not deliver a webhook event to a registered node |

To propose a new standard error code, open a GitHub issue with the
trigger condition, retryability, and an example payload.
