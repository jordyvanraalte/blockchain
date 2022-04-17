from network.blockchain_node import BlockchainNode

import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('--addr', '-a', type=str, help='Defines the address of the application.', default='0.0.0.0')
parser.add_argument('--port','-p', type=int, help='Defines the port of the application.', default=50000)
parser.add_argument('--debug','-d', action="store_true", help='', default=False)
parser.add_argument('--private_key','-pk',action="store", type=str, help='path of private key if private key provided')
parser.add_argument('--public_key','-pubk',action="store", type=str, help='path of public key if public key provided')


args = parser.parse_args()


node = BlockchainNode(args.addr, args.port, args.debug)
node.start()