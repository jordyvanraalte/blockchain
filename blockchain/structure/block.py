import uuid
import jsons
import copy
from .transaction import Transaction, CoinbaseTransaction
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from blockchain.utils import crypto


class Block:
    def __init__(self, index, time_stamp, transactions, previous_block, previous_hash, proof, notes):
        self.id = str(uuid.uuid4())
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

        coinbase_transactions = 0
        for transaction in self.transactions:
            if type(transaction) == dict:
                transaction = jsons.loads(jsons.dumps(transaction), Transaction)

            if type(transaction) == CoinbaseTransaction:
                if coinbase_transactions > 1:
                    return False
                else:
                    coinbase_transactions += 1

            if not transaction.is_valid():
                return False

        if type(self.previous_hash) == str:
            return self.previous_block.calculate_hash() == crypto.base64_decode_bytes(self.previous_hash)
        else:
            return self.previous_block.calculate_hash() == self.previous_hash

    @staticmethod
    def encode(b):
        b = copy.copy(b)
        b.transactions = list(map(lambda i: Transaction.encode(i), b.transactions))
        if b.previous_hash is not None:
            b.previous_hash = crypto.base64_encode_bytes(b.previous_hash)
            b.previous_block = Block.encode(b.previous_block)
        # returns a copy since memory id will be the same, todo change later
        return b

    @staticmethod
    def decode(b):
            b = copy.copy(b)
            b.transactions = list(map(lambda t: Transaction.decode(t), b.transactions))
            if b.previous_hash is not None:
                b.previous_hash = crypto.base64_decode_bytes(b.previous_hash)
                previous_block = jsons.loads(jsons.dumps(b.previous_block), Block)
                b.previous_block = Block.decode(previous_block)
            return b
