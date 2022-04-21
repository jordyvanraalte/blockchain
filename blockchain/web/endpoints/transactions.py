from flask import Blueprint

transactions = Blueprint('transactions', __name__, url_prefix="/api/transactions")


@transactions.route("/", methods=['GET', 'POST'])
def do_transactions():
    return []


@transactions.route("/<id>", methods=['GET'])
def do_transaction(id):
    return []
