import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class AuditEntry:
    index: int
    timestamp: float
    actor_id: str
    action: str
    target_id: str
    metadata: dict
    prev_hash: str
    hash: str = ""

    def calculate_hash(self) -> str:
        """Computes SHA-256 hash of the entry content + prev_hash."""
        # We exclude 'hash' from the calculation itself to avoid recursion
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "actor_id": self.actor_id,
            "action": self.action,
            "target_id": self.target_id,
            "metadata": self.metadata,
            "prev_hash": self.prev_hash
        }
        # Sort keys for consistent JSON serialization
        block_string = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class AuditLedger:
    def __init__(self):
        self.chain: List[AuditEntry] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_entry = AuditEntry(
            index=0,
            timestamp=0.0,
            actor_id="SYSTEM",
            action="GENESIS",
            target_id="ROOT",
            metadata={"info": "Legitimate Origin"},
            prev_hash="0" * 64
        )
        genesis_entry.hash = genesis_entry.calculate_hash()
        self.chain.append(genesis_entry)

    def log_event(self, actor_id: str, action: str, target_id: str, metadata: dict = None) -> AuditEntry:
        if metadata is None:
            metadata = {}
        
        prev_entry = self.chain[-1]
        new_entry = AuditEntry(
            index=prev_entry.index + 1,
            timestamp=time.time(),
            actor_id=actor_id,
            action=action,
            target_id=target_id,
            metadata=metadata,
            prev_hash=prev_entry.hash
        )
        new_entry.hash = new_entry.calculate_hash()
        self.chain.append(new_entry)
        return new_entry

    def validate_chain(self) -> bool:
        """
        Walks the chain and verifies integrity.
        Returns True if valid, False if tampered.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Check Link
            if current.prev_hash != previous.hash:
                print(f"Broken Link at index {i}: {current.prev_hash} != {previous.hash}")
                return False

            # 2. Check Content Integrity
            recalc = current.calculate_hash()
            if current.hash != recalc:
                print(f"Data Tampered at index {i}: {current.hash} != {recalc}")
                return False

        return True

    def get_entries_by_actor(self, actor_id: str) -> List[AuditEntry]:
        return [e for e in self.chain if e.actor_id == actor_id]
