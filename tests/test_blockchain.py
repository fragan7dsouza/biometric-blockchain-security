"""
Unit tests for Simulated Blockchain Ledger and Verifier Submodule.
"""

import pytest
import hashlib
from src.blockchain.blockchain import Blockchain, Transaction, Block
from src.blockchain.verifier import BlockchainVerifier


def test_blockchain_mining_and_validation():
    bc = Blockchain(difficulty=1)
    assert len(bc.chain) == 1  # Genesis block

    tx = Transaction(
        tx_id="tx_test_101",
        user_id_hash=hashlib.sha256(b"user1").hexdigest(),
        ciphertext_hash=hashlib.sha256(b"ciphertext1").hexdigest(),
        encrypted_data_ref="ref://data/101"
    )

    bc.add_transaction(tx)
    mined_block = bc.mine_pending_transactions()

    assert len(bc.chain) == 2
    assert mined_block.index == 1
    assert bc.is_chain_valid() is True


def test_blockchain_verifier():
    bc = Blockchain(difficulty=1)
    verifier = BlockchainVerifier(bc)

    ciphertext_bytes = b"encrypted_payload_data_bytes_12345"
    c_hash = verifier.compute_ciphertext_hash(ciphertext_bytes)

    tx = Transaction(
        tx_id="tx_verify_001",
        user_id_hash=hashlib.sha256(b"user_alice").hexdigest(),
        ciphertext_hash=c_hash,
        encrypted_data_ref="ref://data/001"
    )

    bc.add_transaction(tx)
    bc.mine_pending_transactions()

    # Valid payload test
    ok, msg, metadata = verifier.verify_ciphertext_integrity("tx_verify_001", ciphertext_bytes)
    assert ok is True
    assert "INTEGRITY_VERIFIED" in msg

    # Tampered payload test
    tampered_bytes = b"encrypted_payload_data_bytes_99999"
    ok_t, msg_t, _ = verifier.verify_ciphertext_integrity("tx_verify_001", tampered_bytes)
    assert ok_t is False
    assert "TAMPER_DETECTED" in msg_t
