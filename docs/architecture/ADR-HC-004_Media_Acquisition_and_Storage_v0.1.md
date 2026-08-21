# ADR-HC-004 — Media Acquisition and Storage v0.1

## Status
`PROPOSED — PROJECT OWNER APPROVAL REQUIRED`

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
