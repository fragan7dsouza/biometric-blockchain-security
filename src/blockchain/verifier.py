"""
Blockchain Data Integrity Verifier Submodule.
Verifies encrypted data payload against immutable blockchain metadata.
Detects tampering and validates data provenance.
"""

import hashlib
from typing import Dict, Any, Tuple, Optional
from src.blockchain.blockchain import Blockchain, Transaction


class BlockchainVerifier:
    """
    Verifies that encrypted data payloads match the immutable hash recorded on the blockchain ledger.
    """

    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain

    def compute_ciphertext_hash(self, ciphertext_bytes: bytes) -> str:
        """Computes SHA-256 hash of raw ciphertext bytes."""
        return hashlib.sha256(ciphertext_bytes).hexdigest()

    def verify_ciphertext_integrity(
        self,
        tx_id: str,
        ciphertext_bytes: bytes
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Verifies if ciphertext_bytes match the metadata stored in tx_id on the blockchain.

        Returns:
            (is_valid: bool, status_msg: str, metadata: dict)
        """
        # 1. Verify overall blockchain health
        if not self.blockchain.is_chain_valid():
            return False, "BLOCKCHAIN_INVALID: Ledger chain integrity check failed.", {}

        # 2. Locate transaction on chain
        tx = self.blockchain.find_transaction_by_id(tx_id)
        if tx is None:
            return False, f"TX_NOT_FOUND: Transaction ID '{tx_id}' not found on blockchain.", {}

        # 3. Compute current ciphertext SHA-256 hash
        current_hash = self.compute_ciphertext_hash(ciphertext_bytes)

        # 4. Compare current hash with on-chain record
        if current_hash == tx.ciphertext_hash:
            return True, "INTEGRITY_VERIFIED: Ciphertext hash matches blockchain record perfectly.", tx.to_dict()
        else:
            return False, (
                f"TAMPER_DETECTED: Computed hash ({current_hash[:16]}...) does NOT match "
                f"on-chain record ({tx.ciphertext_hash[:16]}...)."
            ), tx.to_dict()
