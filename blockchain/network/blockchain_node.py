import time

import jsons
from apscheduler.schedulers.background import BackgroundScheduler
from blockchain.structure.block import Block
from blockchain.structure.blockchain import Blockchain
from blockchain.structure.transaction import Transaction
from blockchain.network.node import Node
from blockchain.network import protocol


# todo block class contains previous block which can result in large structures send through to the connection. Change the block class
class BlockchainNode(Node):
    def __init__(self, addr, port, wallet, debug=False, difficulty=2):
        super().__init__(addr, port, debug=debug)
        self.blockchain = Blockchain(difficulty)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.ping, 'interval', seconds=30)
        self.scheduler.start()
        self.wallet = wallet

    def ping(self):
        self.broadcast(protocol.ping())
        # self.resolve_conflicts_broadcast()

    def resolve_conflicts_broadcast(self):
        self.broadcast(protocol.chain_request())

    def add_transaction(self, transaction):
        is_new_transaction = self.blockchain.new_transaction(transaction)
        if is_new_transaction:
            self.broadcast(protocol.new_transaction(Transaction.encode(transaction)))

    def mine(self):
        block = self.blockchain.mine(self.wallet.address)
        if block is not None:
            self.broadcast(protocol.new_block(Block.encode(block)))

    # todo whole chain gets sends but seems unreasonable, figure out how the chain gets send in the network
    # todo solve double chain problem by adding missing transactions back to the transaction pool
    def resolve_conflicts(self, node, new_blockchain):
        if len(new_blockchain.chain) > len(self.blockchain.chain) and new_blockchain.is_valid_chain():
            self.debug_print(f'New chain found on: {node.id}')

            if self.blockchain.mining:
                self.blockchain.mining = False
                time.sleep(1)

            self.blockchain = new_blockchain
            return True
        return False

    def node_message(self, node, data):
        self.debug_print("node_message: " + node.id + ": " + str(data))
        if data['type'] == protocol.CHAIN_REQUEST:
            self.on_chain_request(node)
        elif data['type'] == protocol.CHAIN_RESPONSE:
            self.on_chain_received(node, data['blockchain'])
        elif data['type'] == protocol.NEW_TRANSACTION:
            self.on_transaction_received(data['transaction'])
        elif data['type'] == protocol.NEW_BLOCK:
            self.on_block_received(data['block'])
        elif data['type'] == protocol.PING:
            self.on_ping_receive(node)

    def on_chain_request(self, node):
        self.send(node, protocol.chain_response(self.blockchain.encode()))

    def on_ping_receive(self, node):
        self.send(node, protocol.pong())

    def on_chain_received(self, node, blockchain):
        blockchain = jsons.loads(jsons.dumps(blockchain), Blockchain)
        self.resolve_conflicts(node, blockchain.decode())

    def on_block_received(self, block):
        block = jsons.loads(jsons.dumps(block), Block)
        is_new_block_and_valid = self.blockchain.new_block(Block.decode(block))
        if is_new_block_and_valid:
            self.broadcast(protocol.new_block(block))

    def on_transaction_received(self, transaction):
        transaction = jsons.loads(jsons.dumps(transaction), Transaction)
        self.add_transaction(Transaction.decode(transaction))


if __name__ == '__main__':
    node1 = BlockchainNode('0.0.0.0', 34203, debug=True)
    node1.start()

    node2 = BlockchainNode('0.0.0.0', 50432, debug=True)
    node2.start()
    node2.connect('0.0.0.0', 34203)

    node3 = BlockchainNode('0.0.0.0', 33423, debug=True)
    node3.start()
    node3.connect('0.0.0.0', 34203)
