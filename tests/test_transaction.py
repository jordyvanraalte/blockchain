import unittest
from blockchain.structure.transaction import Transaction
from blockchain.structure.wallet import Wallet


class TestTransaction(unittest.TestCase):
    def test_transaction(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        self.assertTrue(transaction.is_valid())

    def test_greater_input_transaction(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1.2)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        self.assertTrue(transaction.is_valid())

    def test_third_party_signing(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()
        wallet3 = Wallet()
        wallet3.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.add_multi_signing_address(wallet3.address)
        transaction.sign(wallet1.private_key)
        transaction.sign(wallet3.private_key)

        self.assertTrue(transaction.is_valid())

    def test_multiple_input(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()
        wallet3 = Wallet()
        wallet3.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_input(wallet2.address, 1)
        transaction.add_output(wallet3.address, 1)
        transaction.sign(wallet1.private_key)
        transaction.sign(wallet2.private_key)

        self.assertTrue(transaction.is_valid())

    def test_greater_output(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1.1)
        transaction.sign(wallet1.private_key)

        self.assertFalse(transaction.is_valid())

    def test_wrong_signatures(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet2.private_key)

        self.assertFalse(transaction.is_valid())

    def test_negative_values(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, -1)
        transaction.add_output(wallet2.address, -1)
        transaction.sign(wallet1.private_key)

        self.assertFalse(transaction.is_valid())

    def test_tampering(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()
        wallet3 = Wallet()
        wallet3.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)
        transaction.outputs[0] = (wallet3.address, 1)

        self.assertFalse(transaction.is_valid())
