"""
Simulated Blockchain Submodule.
Implements Transaction, Block, and Blockchain data structures with SHA-256 hashing
and Proof-of-Work consensus algorithm. Stores privacy-preserving metadata only.
"""

import time
import json
import hashlib
from typing import List, Dict, Any, Optional


class Transaction:
    """
    Represents a metadata-only transaction on the blockchain.
    Raw facial biometrics and secret keys are NEVER stored on-chain.
    """

    def __init__(
        self,
        tx_id: str,
        user_id_hash: str,
        ciphertext_hash: str,
        encrypted_data_ref: str,
        algo_version: str = "Biometric-GA-LFSR-AES256GCM-v1.0",
        timestamp: Optional[float] = None
    ):
        self.tx_id = tx_id
        self.user_id_hash = user_id_hash
        self.ciphertext_hash = ciphertext_hash
        self.encrypted_data_ref = encrypted_data_ref
        self.algo_version = algo_version
        self.timestamp = timestamp or time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            'tx_id': self.tx_id,
            'user_id_hash': self.user_id_hash,
            'ciphertext_hash': self.ciphertext_hash,
            'encrypted_data_ref': self.encrypted_data_ref,
            'algo_version': self.algo_version,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        return cls(
            tx_id=data['tx_id'],
            user_id_hash=data['user_id_hash'],
            ciphertext_hash=data['ciphertext_hash'],
            encrypted_data_ref=data['encrypted_data_ref'],
            algo_version=data.get('algo_version', 'Biometric-GA-LFSR-AES256GCM-v1.0'),
            timestamp=data.get('timestamp')
        )


class Block:
    """
    Represents a single Block in the Blockchain ledger.
    """

    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: Optional[float] = None,
        nonce: int = 0
    ):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Computes SHA-256 hash of block header and contents.
        """
        block_dict = {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        block_string = json.dumps(block_dict, sort_keys=True)
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty: int) -> str:
        """
        Proof-of-Work mining algorithm.
        Finds a nonce such that block hash starts with 'difficulty' zeros.
        """
        target_prefix = '0' * difficulty
        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
        return self.hash

    def to_dict(self) -> Dict[str, Any]:
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        txs = [Transaction.from_dict(tx) for tx in data['transactions']]
        block = cls(
            index=data['index'],
            transactions=txs,
            previous_hash=data['previous_hash'],
            timestamp=data['timestamp'],
            nonce=data['nonce']
        )
        block.hash = data['hash']
        return block


class Blockchain:
    """
    Manages the chain of blocks, mining, transaction recording, and chain validation.
    """

    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self._create_genesis_block()

    def _create_genesis_block(self):
        """Creates the initial Genesis block."""
        genesis_tx = Transaction(
            tx_id="tx_genesis_0000",
            user_id_hash=hashlib.sha256(b"genesis_user").hexdigest(),
            ciphertext_hash=hashlib.sha256(b"genesis_ciphertext").hexdigest(),
            encrypted_data_ref="ref://genesis",
            timestamp=1700000000.0
        )
        genesis_block = Block(
            index=0,
            transactions=[genesis_tx],
            previous_hash="0" * 64,
            timestamp=1700000000.0
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        """Adds transaction to pending list."""
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self) -> Block:
        """
        Mines all pending transactions into a new Block and appends to the chain.
        """
        if not self.pending_transactions:
            raise ValueError("No pending transactions to mine.")

        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self) -> bool:
        """
        Validates integrity of the entire blockchain.
        Returns True if all hashes, previous hashes, and PoW constraints are valid.
        """
        target_prefix = '0' * self.difficulty
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify current block hash
            if current.hash != current.compute_hash():
                return False

            # 2. Verify link to previous block
            if current.previous_hash != previous.hash:
                return False

            # 3. Verify Proof-of-Work
            if not current.hash.startswith(target_prefix):
                return False

        return True

    def find_transaction_by_id(self, tx_id: str) -> Optional[Transaction]:
        """Searches blockchain for a transaction by ID."""
        for block in self.chain:
            for tx in block.transactions:
                if tx.tx_id == tx_id:
                    return tx
        return None

    def to_json(self) -> str:
        """Serializes chain to JSON string."""
        return json.dumps({
            'difficulty': self.difficulty,
            'chain': [block.to_dict() for block in self.chain]
        }, indent=2)

    def save_to_file(self, file_path: str):
        """Saves chain to JSON file."""
        data = {
            'difficulty': self.difficulty,
            'chain': [block.to_dict() for block in self.chain]
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: str) -> 'Blockchain':
        """Loads chain from JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        bc = cls(difficulty=data.get('difficulty', 2))
        bc.chain = [Block.from_dict(b) for b in data['chain']]
        return bc
