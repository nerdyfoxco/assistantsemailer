import unittest
import time
from chain import AuditLedger, AuditEntry

class TestAuditLedger(unittest.TestCase):

    def setUp(self):
        self.ledger = AuditLedger()

    def test_01_genesis_block(self):
        """Chain should start with a genesis block."""
        self.assertEqual(len(self.ledger.chain), 1)
        self.assertEqual(self.ledger.chain[0].action, "GENESIS")

    def test_02_log_event(self):
        """Logging an event should append to chain."""
        entry = self.ledger.log_event("user_1", "LOGIN", "session_1")
        self.assertEqual(len(self.ledger.chain), 2)
        self.assertEqual(entry.index, 1)

    def test_03_chain_integrity_success(self):
        """Untampered chain should validate True."""
        self.ledger.log_event("u1", "A", "t1")
        self.ledger.log_event("u2", "B", "t2")
        self.assertTrue(self.ledger.validate_chain())

    def test_04_tamper_data_detect(self):
        """Modifying data in a block should break validation."""
        self.ledger.log_event("u1", "A", "t1")
        # Attack!
        self.ledger.chain[1].action = "EVIL_ACTION"
        self.assertFalse(self.ledger.validate_chain())

    def test_05_tamper_prev_hash_detect(self):
        """Modifying link should break validation."""
        self.ledger.log_event("u1", "A", "t1")
        self.ledger.log_event("u2", "B", "t2")
        # Break the link
        self.ledger.chain[2].prev_hash = "fake_hash"
        self.assertFalse(self.ledger.validate_chain())

    def test_06_verify_genesis_hash(self):
        """Genesis block should have valid self-hash."""
        genesis = self.ledger.chain[0]
        self.assertEqual(genesis.hash, genesis.calculate_hash())

    def test_07_metadata_integrity(self):
        """Metadata is part of the hash."""
        self.ledger.log_event("u1", "A", "t1", {"ip": "1.2.3.4"})
        self.assertTrue(self.ledger.validate_chain())
        # Tamper metadata
        self.ledger.chain[1].metadata["ip"] = "5.6.7.8"
        self.assertFalse(self.ledger.validate_chain())

    def test_08_actor_filter(self):
        """Can filter logs by actor."""
        self.ledger.log_event("alice", "A", "t1")
        self.ledger.log_event("bob", "B", "t2")
        self.ledger.log_event("alice", "C", "t3")
        
        alice_logs = self.ledger.get_entries_by_actor("alice")
        self.assertEqual(len(alice_logs), 2)
        self.assertEqual(alice_logs[0].action, "A")
        self.assertEqual(alice_logs[1].action, "C")

    def test_09_timestamp_Monotonicity(self):
        """Timestamps should (generally) increase."""
        # This is a loose check as time.time() is fast
        e1 = self.ledger.log_event("u1", "1", "1")
        time.sleep(0.01)
        e2 = self.ledger.log_event("u1", "2", "2")
        self.assertGreater(e2.timestamp, e1.timestamp)

    def test_10_recalc_hash_consistency(self):
        """calculate_hash should be deterministic."""
        entry = self.ledger.log_event("u1", "A", "t1")
        h1 = entry.calculate_hash()
        h2 = entry.calculate_hash()
        self.assertEqual(h1, h2)

if __name__ == '__main__':
    unittest.main()
