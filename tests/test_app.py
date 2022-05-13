import unittest

import jsons

from blockchain.network.blockchain_node import BlockchainNode
from blockchain.structure.transaction import Transaction
from blockchain.structure.wallet import Wallet
from blockchain.app import run, App
import time


class TestApp(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.app = App('0.0.0.0', 50000, self.wallet, False)
        self.app.node.start()
        self.context = self.app.app.app_context()
        self.context.push()
        self.client = self.app.app.test_client()

    def tearDown(self):
        self.context.pop()
        self.app.node.stop()
        self.app.node.join()

    def test_add_transaction(self):
        wallet1 = Wallet()
        wallet1.create_keys()

        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        json = jsons.loads(jsons.dumps(Transaction.encode(transaction)))

        response = self.client.post('/api/transactions', json=json)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(self.app.node.blockchain.transaction_pool) == 1)
