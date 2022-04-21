from flask import Blueprint

blocks = Blueprint('blocks', __name__, url_prefix="/api/blocks")


@blocks.route("/", methods=['GET', 'POST'])
def do_blocks():
    return []


@blocks.route("/<id>", methods=['GET'])
def do_block(id):
    return []
