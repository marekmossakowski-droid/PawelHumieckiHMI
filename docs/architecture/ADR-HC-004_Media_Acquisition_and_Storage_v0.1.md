# ADR-HC-004 — Media Acquisition and Storage v0.1

## Status
`APPROVED / BASELINED — PR #4`

Approved PR head: `26c66a0e2ada0348c7204516c02f4c8b0581f38f`  
Canonical merge SHA: `c2493ef39a1b45b934cd2dc001279db110a17fc0`

## Decision
Images captured during treatment SHALL be immutable evidence objects linked to a specific session with provenance metadata. `BEFORE`, `AFTER` and reference/example media SHALL be distinct categories.

The HMI SHALL initiate or present media capture, while durable media storage and indexing SHALL reside in the local edge/data layer. Reference images SHALL never be silently presented as actual-animal evidence.

## Required metadata
- media identifier;
- session identifier;
- animal identifier when resolved;
- capture/import timestamp;
- source/device where available;
- category and provenance.

## MVP
Bench MVP uses test media only. Camera vendor, transport and codec remain downstream choices.
