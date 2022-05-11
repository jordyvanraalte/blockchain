import unittest
from blockchain.network.blockchain_node import BlockchainNode
from blockchain.structure.transaction import Transaction
from blockchain.structure.wallet import Wallet
import time


class TestBlockchainNode(unittest.TestCase):
    def test_new_transaction(self):


        self.assertTrue(len(node1.blockchain.transaction_pool) == 1)
