import unittest
import datetime
from blockchain.structure.blockchain import Blockchain, DIFFICULTY
from blockchain.structure.transaction import Transaction
from blockchain.structure.block import Block
from blockchain.structure.wallet import Wallet


class TestBlockchain(unittest.TestCase):
    def test_chain(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        blockchain.new_transaction(transaction)

        blockchain.mine()

        self.assertTrue(blockchain.is_valid_chain() and len(blockchain.chain) == 2)

    def test_mining(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        blockchain.new_transaction(transaction)

        block = blockchain.mine()
        self.assertTrue(
            block.calculate_hash()[:DIFFICULTY] == bytes(''.join('\x00' for i in range(DIFFICULTY)), 'utf-8'))

    def test_longer_chain(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_input(wallet1.address, 1)
        transaction1.add_output(wallet2.address, 1)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)

        transaction3 = Transaction()
        transaction3.add_input(wallet1.address, 1)
        transaction3.add_output(wallet2.address, 1)
        transaction3.sign(wallet1.private_key)

        blockchain.new_transaction(transaction1)
        blockchain.mine()

        blockchain.new_transaction(transaction2)
        blockchain.mine()

        self.assertTrue(blockchain.is_valid_chain())

    def test_tampering(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_input(wallet1.address, 1)
        transaction1.add_output(wallet2.address, 1)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)

        transaction3 = Transaction()
        transaction3.add_input(wallet1.address, 1)
        transaction3.add_output(wallet2.address, 1)
        transaction3.sign(wallet1.private_key)

        blockchain.new_transaction(transaction1)
        blockchain.mine()

        blockchain.new_transaction(transaction2)
        blockchain.mine()

        blockchain.chain[1].transactions.append(transaction3)

        self.assertFalse(blockchain.is_valid_chain())

    def test_non_valid_proof(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        block = Block(1, datetime.datetime.now(), [transaction], blockchain.last_block,
                      blockchain.last_block.calculate_hash(), 1, '')

        self.assertFalse(blockchain.new_block(block))

    def test_non_valid_transaction_block(self):
        blockchain = Blockchain()

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_input(wallet1.address, 1)
        transaction1.add_output(wallet2.address, -1)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet2.address, 1)
        transaction2.add_output(wallet1.address, -1)
        transaction2.sign(wallet1.private_key)

        block = Block(1, datetime.datetime.now(), [transaction1, transaction2], blockchain.last_block,
                      blockchain.last_block.calculate_hash(), 1, '')

        self.assertFalse(blockchain.new_block(block))
