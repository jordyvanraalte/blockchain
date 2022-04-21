from .network.blockchain_node import BlockchainNode
from .web.server import Server


def run(addr, port, debug):
    node = BlockchainNode(addr, port, debug)
    node.start()

    server = Server('0.0.0.0', 8080)
    server.start()
