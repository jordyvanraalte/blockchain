from blockchain.structure.block import Block
import datetime

DIFFICULTY = 5


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transaction_pool = []
        self.last_block = self.create_block(None, None, 1, [])

    def create_block(self, previous_block, previous_hash, proof, verified_transactions):
        block = Block(
            len(self.chain),
            datetime.datetime.now(),
            verified_transactions,
            previous_block,
            previous_hash,
            proof)
        # self.chain.append(block)
        # self.last_block = block
        return block

    # todo stop mining of block has been found.
    # todo broadcast verified transactions
    def mine(self):
        # first verify transactions:
        verified_transaction = []
        for transaction in self.transaction_pool:
            if transaction.is_valid():
                verified_transaction.append(transaction)

        block = None
        if len(verified_transaction) >= 1:
            block = self.create_block(self.last_block, self.last_block.calculate_hash(), 1, verified_transaction)
            while True:
                hash = block.calculate_hash()
                if hash[:DIFFICULTY]:
                    break
                else:
                    block.proof += 1
        else:
            return block

        self.chain.append(block)
        self.last_block = block
        return block

    def new_block(self, block):
        if block.is_valid():
            self.chain.append(block)
            self.last_block = block

    def new_transaction(self, transaction):
        self.transaction_pool.append(transaction)

    def is_valid_chain(self):
        for block in self.chain:
            if not block.is_valid():
                return False

        return True
