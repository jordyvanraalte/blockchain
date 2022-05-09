import unittest
from blockchain.network.blockchain_node import BlockchainNode
from blockchain.structure.transaction import Transaction
from blockchain.structure.wallet import Wallet
import time


class TestBlockchainNode(unittest.TestCase):
    def test_new_transaction(self):
        node_wallet = Wallet()
        node_wallet.create_keys()

        node1 = BlockchainNode('0.0.0.0', 50001, node_wallet)
        node2 = BlockchainNode('0.0.0.0', 50002, node_wallet)
        node3 = BlockchainNode('0.0.0.0', 50003, node_wallet)
        node4 = BlockchainNode('0.0.0.0', 50004, node_wallet)
        node5 = BlockchainNode('0.0.0.0', 50005, node_wallet)

        node1.start()
        node2.start()
        node3.start()
        node4.start()
        node5.start()

        node1.connect('0.0.0.0', 50002)
        node1.connect('0.0.0.0', 50003)
        node2.connect('0.0.0.0', 50004)

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        node1.add_transaction(transaction)

        time.sleep(1)

        node1.stop()
        node2.stop()
        node3.stop()
        node4.stop()
        node5.stop()

        time.sleep(1)

        node1.join()
        node2.join()
        node3.join()
        node4.join()
        node5.join()

        self.assertTrue(len(node1.blockchain.transaction_pool) == 1)
        self.assertTrue(len(node2.blockchain.transaction_pool) == 1)
        self.assertTrue(len(node4.blockchain.transaction_pool) == 1)
        self.assertTrue(len(node5.blockchain.transaction_pool) == 0)

    def test_new_block(self):
        node_wallet = Wallet()
        node_wallet.create_keys()

        node1 = BlockchainNode('0.0.0.0', 50001, node_wallet)
        node2 = BlockchainNode('0.0.0.0', 50002, node_wallet)
        node3 = BlockchainNode('0.0.0.0', 50003, node_wallet)
        node4 = BlockchainNode('0.0.0.0', 50004, node_wallet)
        node5 = BlockchainNode('0.0.0.0', 50005, node_wallet)

        node1.start()
        node2.start()
        node3.start()
        node4.start()
        node5.start()

        node1.connect('0.0.0.0', 50002)
        node1.connect('0.0.0.0', 50003)
        node2.connect('0.0.0.0', 50004)

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction = Transaction()
        transaction.add_input(wallet1.address, 1)
        transaction.add_output(wallet2.address, 1)
        transaction.sign(wallet1.private_key)

        node1.add_transaction(transaction)
        node1.mine()

        time.sleep(1)

        node1.stop()
        node2.stop()
        node3.stop()
        node4.stop()
        node5.stop()

        time.sleep(1)

        node1.join()
        node2.join()
        node3.join()
        node4.join()
        node5.join()

        self.assertTrue(len(node1.blockchain.chain) == 2)
        self.assertTrue(len(node2.blockchain.chain) == 2)
        self.assertTrue(len(node4.blockchain.chain) == 2)
        self.assertTrue(len(node5.blockchain.chain) == 1)


    def test_resolve_conflicts(self):
        node_wallet = Wallet()
        node_wallet.create_keys()

        node1 = BlockchainNode('0.0.0.0', 50001, node_wallet)
        node2 = BlockchainNode('0.0.0.0', 50002, node_wallet)

        node1.start()
        node2.start()

        node1.connect('0.0.0.0', 50002)

        wallet1 = Wallet()
        wallet1.create_keys()
        wallet2 = Wallet()
        wallet2.create_keys()

        transaction1 = Transaction()
        transaction1.add_input(wallet1.address, 1)
        transaction1.add_output(wallet2.address, 1)
        transaction1.sign(wallet1.private_key)

        node1.add_transaction(transaction1)
        node1.mine()

        time.sleep(1)

        transaction2 = Transaction()
        transaction2.add_input(wallet1.address, 1)
        transaction2.add_output(wallet2.address, 1)
        transaction2.sign(wallet1.private_key)

        node1.add_transaction(transaction2)

        node3 = BlockchainNode('0.0.0.0', 50003, node_wallet)
        node4 = BlockchainNode('0.0.0.0', 50004, node_wallet)

        node3.connect('0.0.0.0', 50001)
        node3.resolve_conflicts_broadcast()

        time.sleep(2)

        node1.stop()
        node2.stop()

        time.sleep(1)

        node1.join()
        node2.join()

        self.assertTrue(len(node1.blockchain.chain) == 2)
        self.assertTrue(len(node3.blockchain.chain) == 2)
        self.assertTrue(len(node4.blockchain.chain) == 1)