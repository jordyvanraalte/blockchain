import datetime
from blockchain.structure.block import Block
from blockchain.structure.transaction import Transaction

DIFFICULTY = 2
PUBLIC_ADDRESS_GENESIS_BLOCK = "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF5bXYzdFlaVDZPUVlxM2lUaTJMSgpEbzgxMVVaNzQyV2NjOTQ4Q21IcHlHa0NKTi9iVld0YWo2TUtuNzZCdERFTm5HSW4vUjYwWWtlNERaekwzTUJDCjU4T0lvWC9GL2ZEaUZqSzk0WHZjdFlac0o3OGhONi8yMGVabGF4Yk81S1RhbnhpOHVINGN6OHBLajc1TnlXOUcKOEVPZUk2WnRuTVR5b1lyUkFCZTZ0R21qWElnQUZKaG1SbE54bnpIVWVGRXlxaDhHZko3aUdhQ0lyQmRKUGZVaQpLc2Zoakg1ZVlNUnZTbjNrN2F4UWlwb2lIYTN3bHU3Qk0rWTZwWjZES1pNVWpsRC8vamJ2Z2krQTlBNDZmKzNECnBWQjI4eStjWU93TXZHdjMydy9BOEJXdzNrZU5mSlQzU0ViSEVQL3BFUk5BUFJsVUVOOHQzbDBVRHV5Q21NRDYKWFFJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="


# todo change chain to a SQLITE database.

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_pool = []

        # creating genesis transaction
        genesis_transaction = Transaction()
        genesis_transaction.add_output(PUBLIC_ADDRESS_GENESIS_BLOCK, 1000)
        self.last_block = self.create_block(None, None, 1, [genesis_transaction], "I'm the Genesis block")

    def new_block(self, block):
        if block.is_valid() and self.is_hash_of_block_valid(block):
            self.chain.append(block)
            self.last_block = block
            return True
        return False

    def create_block(self, previous_block, previous_hash, proof, verified_transactions, notes):
        block = Block(
            len(self.chain),
            datetime.datetime.now(),
            verified_transactions,
            previous_block,
            previous_hash,
            proof,
            notes)
        self.chain.append(block)
        self.last_block = block
        self.transaction_pool = []
        return block

    # todo stop mining of block has been found.
    # todo broadcast verified transactions
    # todo add coinbase reward
    def mine(self):
        # first verify transactions:
        verified_transaction = []
        for transaction in self.transaction_pool:
            if transaction.is_valid():
                verified_transaction.append(transaction)

        block = None
        if len(verified_transaction) >= 1:
            block = self.create_block(self.last_block, self.last_block.calculate_hash(), 1, verified_transaction, '')
            while True:
                hash = block.calculate_hash()
                if hash[:DIFFICULTY] == bytes(''.join('\x00' for i in range(DIFFICULTY)), 'utf-8'):
                    break
                else:
                    block.proof += 1
        else:
            return block

        return block

    def new_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def is_valid_chain(self):
        for block in self.chain:
            if not block.is_valid():
                return False

            if block.previous_block is not None:
                if not self.is_hash_of_block_valid(block):
                    return False

        return True

    def is_hash_of_block_valid(self, block):
        return block.calculate_hash()[:DIFFICULTY] == bytes(''.join('\x00' for i in range(DIFFICULTY)),
                                                 'utf-8')
