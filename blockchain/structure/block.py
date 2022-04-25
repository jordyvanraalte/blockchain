from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes


class Block:
    def __init__(self, index, time_stamp, transactions, previous_block, previous_hash, proof, notes):
        self.index = index
        self.time_stamp = time_stamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.previous_block = previous_block
        self.proof = proof
        self.notes = notes

    def __repr__(self):
        return f"index : {self.index}, time_stamp: {self.time_stamp}, transactions: {self.transactions}, previous_hash: {self.previous_hash}, proof: {self.proof}, notes: {self.notes}"

    def calculate_hash(self):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(bytes(str(self.index), 'utf-8'))
        digest.update(bytes(str(self.time_stamp), 'utf-8'))
        digest.update(bytes(str(self.transactions), 'utf-8'))
        digest.update(bytes(str(self.previous_hash), 'utf-8'))
        digest.update(bytes(str(self.proof), 'utf-8'))
        return digest.finalize()

    def is_valid(self):
        if self.previous_block is None:
            return True

        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        return self.previous_block.calculate_hash() == self.previous_hash
