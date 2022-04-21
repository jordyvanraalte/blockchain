from flask import Blueprint

nodes = Blueprint('nodes', __name__, url_prefix="/api/nodes")


@nodes.route("/", methods=['GET', 'POST'])
def do_nodes():
    return []


@nodes.route("/<id>", methods=['GET'])
def do_node(id):
    return []

