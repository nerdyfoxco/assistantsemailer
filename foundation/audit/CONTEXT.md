# UMP-00-03: Immutable Audit Ledger

## Purpose
To create a tamper-evident record of ALL system actions (User, AI, HITL). Each log entry is cryptographically linked to the previous one, forming a blockchain-style ledger.

## Context
"Crypto-enforced auditability."
We need to prove who did what, when, and that the history hasn't been rewritten.

## Requirements
1.  **Structure**: `AuditEntry` with `prev_hash`, `timestamp`, `actor`, `action`, `target`, `metadata`.
2.  **Hashing**: SHA-256 of the JSON representation of the entry + previous hash.
3.  **Verification**: `validate_chain()` function that walks the chain and recomputes hashes to detect tampering.
4.  **Immutability**: Appending is allowed. Modifying is impossible without breaking the chain.

## Verification
10-Test Suite (`test_audit.py`):
- Create chain.
- Append entries.
- Verify validity.
- Tamper with middle entry -> Verification fails.
- Tamper with last entry -> Verification fails.
