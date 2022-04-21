from flask import Flask
from .endpoints import block, mine, nodes, transactions


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port

        self.app = Flask(__name__)
        self.app.register_blueprint(block.blocks)
        self.app.register_blueprint(mine.mine)
        self.app.register_blueprint(nodes.nodes)
        self.app.register_blueprint(transactions.transactions)

    def start(self):
        self.app.run(host=self.addr, port=self.port)
