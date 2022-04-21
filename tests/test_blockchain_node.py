import unittest
from blockchain.network.blockchain_node import BlockchainNode
from blockchain.structure.transaction import Transaction
import time


class TestBlockchainNode(unittest.TestCase):
    def test_new_transaction(self):
        node1 = BlockchainNode('0.0.0.0', 50001, debug=True)
        node2 = BlockchainNode('0.0.0.0', 50002, debug=True)
        node3 = BlockchainNode('0.0.0.0', 50003, debug=True)

        node1.start()
        node2.start()
        node3.start()

        node1.connect('0.0.0.0', 50002)
        node1.connect('0.0.0.0', 50003)

        node1.add_transaction(Transaction("123", 10, "Peter", "Steve"))
        time.sleep(1)

        node1.stop()
        node2.stop()
        node3.stop()

        self.assertTrue(len(node2.blockchain.transaction_pool) == 1)
        self.assertTrue(len(node3.blockchain.transaction_pool) == 1)

    def test_resolve_conflicts(self):
        node1 = BlockchainNode('0.0.0.0', 50001, debug=True)
        node2 = BlockchainNode('0.0.0.0', 50002, debug=True)
        node3 = BlockchainNode('0.0.0.0', 50003, debug=True)

        node1.start()
        node2.start()
        node3.start()

        node1.connect('0.0.0.0', 50002)
        node1.connect('0.0.0.0', 50003)

        time.sleep(1)

    def test_mining(self):
        node1 = BlockchainNode('0.0.0.0', 50001, debug=True)
        node2 = BlockchainNode('0.0.0.0', 50002, debug=True)
        node3 = BlockchainNode('0.0.0.0', 50003, debug=True)

        node1.start()
        node2.start()
        node3.start()

        node1.connect('0.0.0.0', 50002)
        node1.connect('0.0.0.0', 50003)

        time.sleep(1)
