# MEP Bot Federation Specification
### draft-mep-federation-01

Status: Draft  
Last updated: 2026-08-13  
Spec version: `mep.federation.v1`

## Abstract

This document defines the public-safe protocol boundary used when one bot owner
publishes a bot for discovery and another bot requests a collaboration. It
complements `mep.node-connectivity.v1`: connectivity establishes reachability,
while federation describes what may be discovered and how an invitation moves
through explicit, expiring states.

Federation messages do not authorize repository access or code execution. A
product such as Deskbot may translate an accepted invitation into a separate,
locally enforced collaboration grant after both owners approve the relevant
resources.

## 1. Scope

This draft specifies:

- public-safe bot profiles;
- owner-selected discovery visibility;
- lifecycle, reachability, readiness, and availability distinctions;
- direct collaboration invitations and bounded counteroffers;
- accept, reject, revoke, and expiry semantics;
- replay and recipient-binding requirements; and
- the non-executing preview grant used before resource authorization.

This draft does not specify:

- repository credentials or source transfer;
- remote shell or tool execution;
- payments, escrow, or settlement;
- a global reputation score; or
- automatic acceptance by unknown requesters.

## 2. Design principles

### 2.1 Private by default

A bot MUST default to `private`. Presence MUST NOT make a bot discoverable
unless its owner publishes a profile with `visibility` set to `invite_link` or
`discoverable`.

### 2.2 Presence is not permission

`online` means reachable. `provider_ready` means locally configured to evaluate
invitations. `available` means willing to receive invitations. None of these
states grants permission to execute work.

### 2.3 Two authorities remain separate

The bot owner controls bot compute, model usage, time, and local capabilities.
The requester controls repository and task data. Accepting an invitation grants
neither party the other party's credentials or resources.

### 2.4 Minimum disclosure

Federation messages MUST NOT contain email addresses, local paths, credentials,
private repository names, raw prompts, source code, private reasoning, or model
provider account details. Implementations MAY exchange additional sensitive
terms through a separately authenticated and encrypted product channel.

### 2.5 No execution by message interpretation

Receivers MUST treat all free text and metadata as untrusted data. A federation
message MUST NOT be interpreted as a shell command or tool call. The preview
grant requires `execution_allowed: false`; changing that value requires a future
protocol version or separately specified execution contract.

## 3. Envelope

Every message conforms to `schemas/federation-v1.schema.json` and contains:

- `spec_version`: `mep.federation.v1`;
- `message_id`: globally unique UUID;
- `timestamp_ms`: sender time;
- `expires_at_ms`: event expiry;
- `event_type`: registered federation event;
- `source.node_id`: cryptographic sender identity;
- `target.node_id`: recipient for targeted events, omitted only for profile and
  presence publication; and
- the event-specific object.

Unknown fields follow the MEP v1 unknown-field rule and MUST be ignored unless
they conflict with a required invariant.

## 4. Bot profiles

`bot.profile.publish` contains public-safe metadata:

- stable bot node ID and display name;
- visibility: `private`, `invite_link`, or `discoverable`;
- declared capability tokens;
- acceptance mode: `manual` or `trusted_only`;
- maximum invitation duration and concurrency;
- private-repository support as a boolean; and
- retention policy expressed as hours.

Profiles MUST NOT claim live status. Reachability and readiness are reported by
presence events.

Publishing `visibility: private` is a withdrawal signal. Hubs MUST remove that
profile from discovery results while retaining only the audit data required by
their disclosed retention policy.

## 5. Presence and readiness

`bot.presence.update` reports independent fields:

- `lifecycle`: `approved`, `configured`, `connecting`, `online`,
  `provider_ready`, `degraded`, `offline`, `suspended`, or `revoked`;
- `availability`: `available`, `busy`, `do_not_disturb`, or `offline`;
- `reachable`: whether push delivery currently succeeds; and
- `provider_ready`: whether local policy and runtime checks permit invitation
  evaluation.

A hub MUST advertise a bot as available only when all of these are true:

1. its latest profile is `discoverable` or reached through a valid invite link;
2. `reachable` is true;
3. `provider_ready` is true; and
4. `availability` is `available`.

Presence expires. A hub MUST degrade or remove stale presence according to its
published timeout policy.

## 6. Invitations

`collaboration.invitation.create` starts an invitation in `pending`. It binds:

- one invitation ID;
- one requester node;
- one target bot node;
- requested capability tokens;
- a bounded objective and expected output;
- duration, inference, tool, and retry ceilings;
- a repository disclosure class, not a credential; and
- an expiry time.

The target bot owner may answer with:

- `collaboration.invitation.accept`;
- `collaboration.invitation.reject`; or
- `collaboration.invitation.counter` with reduced or otherwise revised explicit
  terms.

A counteroffer does not silently mutate the invitation. It creates a new
revision, preserves the previous revision, and requires explicit acceptance.
Natural-language discussion cannot change contract fields.

Either source identity may send `collaboration.invitation.revoke` before a
collaboration grant becomes active. Expired, rejected, and revoked invitations
are terminal.

## 7. Preview grant

After an accepted invitation, an implementation may emit
`collaboration.grant.prepare`. In this draft it MUST contain:

```json
{
  "execution_allowed": false,
  "bot_owner_grant": "accepted",
  "requester_resource_grant": "pending",
  "isolation_state": "not_provisioned"
}
```

The fields may later move from `pending` to `accepted` in product-local state,
but this federation draft never authorizes execution. Implementations MUST fail
closed if `execution_allowed` is missing or not false.

## 8. Replay, freshness, and recipient binding

Receivers MUST:

1. verify the source signature using the registered node key;
2. reject expired messages;
3. reject implausibly future-dated messages;
4. persist `(source.node_id, message_id)` for at least the message lifetime;
5. make exact replay idempotent and reject conflicting reuse;
6. verify targeted events name the receiving node; and
7. verify invitation response source and target are the inverse of the
   invitation participants.

Opaque invitation IDs are routing identifiers, not authentication secrets.

## 9. State machine

```text
pending
  -> countered -> pending
  -> accepted -> grant_prepared
  -> rejected
  -> revoked
  -> expired
```

`rejected`, `revoked`, and `expired` are terminal. `grant_prepared` is not an
execution state.

## 10. Product mapping

A conforming Deskbot-style control plane SHOULD:

- store the signed-in account-to-node ownership mapping privately;
- keep the federation node ID as the wire identity;
- show invitations as security decisions rather than ordinary notifications;
- create durable owner-visible audit records;
- require separate bot-owner and requester-resource grants; and
- provision an isolated job environment only under a future execution contract.

The federation transport may be MEP, but the owner control plane remains the
authority for local policy and resource access.

Deskbot's first independent implementation shipped in
[`deskbotdev/deskbot#41`](https://github.com/deskbotdev/deskbot/pull/41). It
implements account-scoped profiles, fresh/provider-ready discovery, durable
invitation revisions, owner decisions, and preview grants. It deliberately does
not implement independent-hub message transport or external execution.

## 11. Conformance

Static conformance fixtures validate message shape. Runtime conformance tests
MUST additionally cover expiry, signature verification, replay, wrong-recipient
delivery, invalid state transitions, and conflicting invitation revisions.
The reference semantic fixtures additionally enforce timestamp ordering,
source/profile identity, invitation participant binding, and response-event
consistency.
