import datetime

import jsons

from blockchain.structure.block import Block
from blockchain.structure.transaction import Transaction, CoinbaseTransaction
import copy

PUBLIC_ADDRESS_GENESIS_BLOCK = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF5bXYzdFlaVDZPUVlxM2lUaTJMSgpEbzgxMVVaNzQyV2NjOTQ4Q21IcHlHa0NKTi9iVld0YWo2TUtuNzZCdERFTm5HSW4vUjYwWWtlNERaekwzTUJDCjU4T0lvWC9GL2ZEaUZqSzk0WHZjdFlac0o3OGhONi8yMGVabGF4Yk81S1RhbnhpOHVINGN6OHBLajc1TnlXOUcKOEVPZUk2WnRuTVR5b1lyUkFCZTZ0R21qWElnQUZKaG1SbE54bnpIVWVGRXlxaDhHZko3aUdhQ0lyQmRKUGZVaQpLc2Zoakg1ZVlNUnZTbjNrN2F4UWlwb2lIYTN3bHU3Qk0rWTZwWjZES1pNVWpsRC8vamJ2Z2krQTlBNDZmKzNECnBWQjI4eStjWU93TXZHdjMydy9BOEJXdzNrZU5mSlQzU0ViSEVQL3BFUk5BUFJsVUVOOHQzbDBVRHV5Q21NRDYKWFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="


# todo change chain to a SQLITE database.
# todo initial difficulty
# todo broadcast difficulty across the network based on time
class Blockchain:
    def __init__(self, difficulty):
        self.chain = []
        self.transaction_pool = []
        self.difficulty = difficulty
        self.mining = False
        self.last_block = None

        # creating genesis transaction
        genesis_transaction = Transaction()
        genesis_transaction.add_output(PUBLIC_ADDRESS_GENESIS_BLOCK, 1000)
        self.create_block(None, None, 1, [genesis_transaction], "I'm the Genesis block")

    def __repr__(self):
        return f"chain: {self.chain}, pool: {self.transaction_pool}, last_block {self.last_block}"

    def new_block(self, block):
        if block.is_valid() and self.is_hash_of_block_valid(block) and not any([b.id == block.id for b in self.chain]):
            self.chain.append(block)
            self.last_block = block
            self.__remove_block_transactions_from_pool(block)
            return True
        return False

    def new_transaction(self, transaction):
        if not any([t.id == transaction.id for t in self.transaction_pool]):
            self.transaction_pool.append(transaction)
            return True
        return False

    def __remove_block_transactions_from_pool(self, block):
        for transaction in block.transactions:
            if transaction in self.transaction_pool:
                self.transaction_pool.remove(transaction)

    # todo add timezone to datetime
    def create_block(self, previous_block, previous_hash, proof, verified_transactions, notes):
        block = Block(
            len(self.chain),
            datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            verified_transactions,
            previous_block,
            previous_hash,
            proof,
            notes)
        self.chain.append(block)
        self.last_block = block
        self.transaction_pool = []
        return block

    def mine(self, mining_address):
        # first verify transactions:
        verified_transactions = []
        for transaction in self.transaction_pool:
            if transaction.is_valid():
                verified_transactions.append(transaction)

        transaction = CoinbaseTransaction()
        transaction.add_output(mining_address, 4.04)

        fees = sum(transaction.total_input_amount() - transaction.total_output_amount() for transaction in
                   verified_transactions)
        transaction.add_output(fees, 4.04)

        verified_transactions.append(transaction)

        block = None
        self.mining = True
        # verified_transactions should at least contain coinbase transaction and 1 transaction
        # todo fix hashing decode to utf-8
        if len(verified_transactions) >= 2:
            block = self.create_block(self.last_block, self.last_block.calculate_hash(), 1, verified_transactions, '')
            while self.mining:
                hash = block.calculate_hash()
                if hash[:self.difficulty] == bytes(''.join('\x00' for i in range(self.difficulty)), 'utf-8'):
                    return block
                else:
                    block.proof += 1

            if not self.mining:
                # return all the transactions to the pool if mining is ended and remove new block
                self.transaction_pool.append(block.transactions)
                del self.chain[-1]
                self.last_block = self.chain[-1]

        else:
            return block

        return None

    def is_valid_chain(self):
        for block in self.chain:
            if isinstance(block, dict):
                block = jsons.loads(jsons.dumps(block), Block)

            if not block.is_valid():
                return False

            if block.previous_block is not None:
                if not self.is_hash_of_block_valid(block):
                    return False

        return True

    def is_hash_of_block_valid(self, block):
        return block.calculate_hash()[:self.difficulty] == bytes(''.join('\x00' for i in range(self.difficulty)),
                                                                 'utf-8')

    def encode(self):
        b = copy.copy(self)
        b.transaction_pool = list(map(lambda t: Transaction.encode(t), b.transaction_pool))
        b.chain = list(map(lambda b: Block.encode(b), b.chain))
        b.last_block = Block.encode(b.last_block)
        return b

    def decode(self):
        b = copy.copy(self)
        b.transaction_pool = list(map(lambda t: Transaction.decode(t), b.transaction_pool))
        b.chain = list(map(lambda b: Block.decode(jsons.loads(jsons.dumps(b), Block)), b.chain))
        b.last_block = Block.decode((jsons.loads(jsons.dumps(b.last_block), Block)))
        return b
