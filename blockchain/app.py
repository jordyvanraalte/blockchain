from blockchain.network.blockchain_node import BlockchainNode
from flask import Blueprint, Flask, make_response, request, jsonify
from blockchain.structure.block import Block
from blockchain.structure.transaction import Transaction
from flask import Flask, make_response, request, jsonify
from copy import copy
import jsons


def run(addr, port, wallet, debug):
    app = App(addr, port, wallet, debug)
    app.run()


class App:
    def __init__(self, addr, port, wallet, debug):
        self.app = Flask(__name__)
        self.node = BlockchainNode(addr, port, wallet, debug=debug)
        self.app.add_url_rule('/api/mine', 'api_mine', self.api_mine, methods=['GET'])
        self.app.add_url_rule('/api/chain', 'api_chain', self.api_chain, methods=['GET'])
        self.app.add_url_rule('/api/transactions', 'api_transactions', self.api_transaction_pool,
                              methods=['GET', 'POST'])
        self.app.add_url_rule('/api/resolve', 'api_resolve', self.api_resolve, methods=['GET'])

    def run(self):
        self.node.start()
        self.app.run('0.0.0.0', 8080)

    def api_mine(self):
        self.node.mine()
        return make_response({"status": "activated"}, 201)

    def api_chain(self):
        chain = copy(self.node.blockchain.chain)
        chain = list(map(lambda b: Block.encode(b), chain))
        return jsonify(jsons.loads(jsons.dumps(chain)))

    def api_transaction_pool(self):
        if request.method == 'POST':
            content = request.get_json()
            transaction = Transaction()
            transaction.inputs = content["inputs"]
            transaction.outputs = content["outputs"]
            transaction.multi_signing_addresses = content["multi_signing_addresses"]
            transaction.signatures = content["signatures"]
            self.node.add_transaction(Transaction.decode(transaction))
            return make_response({"status": "created"}, 200)
        else:
            transactions = copy(self.node.blockchain.transaction_pool)
            transactions = list(map(lambda t: Transaction.encode(t), transactions))
            return jsonify(jsons.loads(jsons.dumps(transactions)))

    def api_resolve(self):
        self.node.resolve_conflicts_broadcast()
        return make_response({"status": "broadcasted!"}, 200)
