# IA-HC-001 — Initial Implementation Authority v0.1

## Status

`ACTIVE — APPROVED BY PROJECT OWNER / PR #8`

Approved exact head: `9c939abea6794e2b5a4815c826410eb0166ab535`  
Canonical merge SHA: `0d58eb2921df298114c304295a061547598ae541`

## 1. Purpose

This authority defines the maximum implementation scope for the first HoofCare bench prototype.

## 2. Authorized scope

The authority permits implementation of a local, non-production bench prototype covering:

- HMI screens and navigation;
- local in-memory or local test persistence;
- animal/session data model;
- limb/claw/zone selection;
- lesion catalogue presentation and human-entered classification;
- treatment/material recording;
- simulated or test-only RFID input;
- simulated KVK state inputs;
- image attachment using test media;
- PDF/report generation;
- local audit trail;
- test fixtures and automated tests;
- read-only adapters designed for future KVK signal observation, provided they do not yet connect to a live machine.

## 3. Explicitly NOT authorized

This authority does not permit:

- live KVK I/O of any kind;
- live hydraulic control;
- live valve output;
- gate, strap, winch or lift control;
- modification, bypass or replacement of original KVK PLC logic;
- modification of E-STOP, safety relays, safety PLC or interlocks;
- live write access to any KVK controller;
- automatic veterinary diagnosis;
- medication dosing or treatment execution;
- public deployment, production release, remote control or unattended operation;
- cloud transfer of real farm/animal data;
- storage of real personal or farm-sensitive data without a separate data/privacy decision.

## 4. Read-only KVK boundary

Any future physical integration requires a separate verified interface record demonstrating that the connection is observational and electrically/logically isolated as appropriate. Physical connection to KVK remains blocked until the actual 2013-generation KVK 801-1 has been inspected.

## 5. Engineering constraints

- test-first implementation;
- fail-closed session/data association;
- no safety dependency on HoofCare;
- explicit provenance for test images and records;
- no hidden state-changing path;
- branch + Draft PR workflow;
- exact-head approval before merge.

## 6. Activation record

Project Owner explicitly approved activation in PR #8 on exact head `9c939abea6794e2b5a4815c826410eb0166ab535`. Authority became active only after controlled merge to `main` as `0d58eb2921df298114c304295a061547598ae541`.
