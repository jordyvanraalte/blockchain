from flask import Blueprint

mine = Blueprint('mine', __name__, url_prefix="/api/mine")


@mine.route("/", methods=['GET', 'POST'])
def do_mine():
    return []

