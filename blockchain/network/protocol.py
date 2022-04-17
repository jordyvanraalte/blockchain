# Packets headers
import uuid

CHAIN_REQUEST = "CHAIN_REQUEST"
CHAIN_RESPONSE = "CHAIN_RESPONSE"
NEW_TRANSACTION = "NEW_TRANSACTION"
NEW_BLOCK = "NEW_BLOCK"
PING = "PING"
PONG = "PONG"


def chain_request():
    return {
        "id": str(uuid.uuid4()),
        "type": CHAIN_REQUEST
    }


def chain_response(blockchain):
    return {
        "id": str(uuid.uuid4()),
        "type": CHAIN_RESPONSE,
        "blockchain": blockchain
    }


def new_transaction(transaction):
    return {
        "id": str(uuid.uuid4()),
        "type": NEW_TRANSACTION,
        "transaction": transaction
    }


def new_block(block):
    return {
        "id": str(uuid.uuid4()),
        "type": NEW_BLOCK,
        "block": block
    }


def ping():
    return {
        "id": str(uuid.uuid4()),
        "type": PING
    }


def pong():
    return {
        "id": str(uuid.uuid4()),
        "type": PONG
    }
