from blockchain.network.blockchain_node import BlockchainNode
from blockchain.structure.block import Block
from blockchain.structure.transaction import Transaction
from flask import Flask, make_response, request, jsonify
from copy import copy
import jsons


def run(addr, port, debug):
    node = BlockchainNode(addr, port, debug)
    node.start()

    app = Flask(__name__)

    @app.route("/", methods=['GET'])
    def main():
        return "<h1>Welcome to the blockchain node</h1>"

    @app.route("/api/mine", methods=['GET'])
    def api_mine():
        node.mine()
        return make_response({"status": "activated"}, 201)

    @app.route("/api/chain", methods=['GET'])
    def api_chain():
        chain = copy(node.blockchain.chain)
        chain = list(map(lambda b: Block.encode(b), chain))
        return jsonify(jsons.loads(jsons.dumps(chain)))

    @app.route("/api/transactions", methods=['GET', 'POST'])
    def transaction_pool():
        if request.method == 'POST':
            content = request.get_json()
            transaction = Transaction()
            transaction.inputs = content["inputs"]
            transaction.outputs = content["outputs"]
            transaction.multi_signing_addresses = content["multi_signing_addresses"]
            transaction.signatures = content["signatures"]
            node.add_transaction(Transaction.decode(transaction))
            return make_response({"status": "created"}, 200)
        else:
            transactions = copy(node.blockchain.transaction_pool)
            transactions = list(map(lambda t: Transaction.encode(t), transactions))
            return jsonify(jsons.loads(jsons.dumps(transactions)))

    @app.route("/api/resolve", methods=['GET'])
    def api_resolve():
        node.resolve_conflicts_broadcast()
        return make_response({"status": "broadcasted!"}, 200)

    app.run('0.0.0.0', 8080)

