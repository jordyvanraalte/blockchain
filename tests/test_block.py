import unittest
from blockchain.network.blockchain_node import Block
from blockchain.structure.transaction import Transaction
from blockchain.structure.wallet import Wallet
import datetime


class TestBlock(unittest.TestCase):
    def test_valid_block(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_output(wallet1.address, 100)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)

        transactions1 = [transaction1]
        transactions2 = [transaction2]

        block1 = Block(1, datetime.datetime.now(), transactions1, None, None, 1, "I'm the genesis block")
        block2 = Block(2, datetime.datetime.now(), transactions2, block1, block1.calculate_hash(), 1,
                       "I'm the second block")
        self.assertTrue(block2.is_valid())

    def test_non_valid_block(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()
        wallet3 = Wallet()
        wallet3.create_keys()

        transaction1 = Transaction()
        transaction1.add_output(wallet1.address, 100)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)
        transaction2.outputs[0] = (wallet3.public_key, 1)

        transactions1 = [transaction1]
        transactions2 = [transaction2]

        block1 = Block(1, datetime.datetime.now(), transactions1, None, None, 1, "I'm the genesis block")
        block2 = Block(2, datetime.datetime.now(), transactions2, block1, block1.previous_hash, 1, "I'm the second block")

        self.assertFalse(block2.is_valid())

    def test_tampering(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_output(wallet1.address, 100)
        transaction1.sign(wallet1.private_key)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)

        transactions1 = [transaction1]
        transactions2 = [transaction2]

        block1 = Block(1, datetime.datetime.now(), transactions1, None, None, 1, "I'm the genesis block")
        hash1 = block1.calculate_hash()
        block1.transactions = transactions2
        self.assertNotEqual(block1.calculate_hash(), hash1)
