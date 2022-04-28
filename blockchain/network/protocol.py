# Packets headers
import uuid
import jsons

CHAIN_REQUEST = "CHAIN_REQUEST"
CHAIN_RESPONSE = "CHAIN_RESPONSE"
NEW_TRANSACTION = "NEW_TRANSACTION"
NEW_BLOCK = "NEW_BLOCK"
PING = "PING"
PONG = "PONG"


def chain_request():
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": CHAIN_REQUEST
    })


def chain_response(blockchain):
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": CHAIN_RESPONSE,
        "blockchain": blockchain
    })


def new_transaction(transaction):
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": NEW_TRANSACTION,
        "transaction": transaction
    })


def new_block(block):
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": NEW_BLOCK,
        "block": block
    })


def ping():
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": PING
    }
)

def pong():
    return jsons.dumps({
        "id": str(uuid.uuid4()),
        "type": PONG
    })
