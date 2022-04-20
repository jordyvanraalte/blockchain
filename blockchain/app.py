from .network.blockchain_node import BlockchainNode


def run(addr, port, debug):
    node = BlockchainNode(addr, port, debug)
    node.start()