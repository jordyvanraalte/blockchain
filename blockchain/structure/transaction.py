from blockchain.utils import crypto


class Transaction:
    def __init__(self, id, amount, sender, recipient):
        self.id = id
        self.amount = amount
        self.sender = sender
        self.recipient = recipient
        self.signature = ""

    def sign(self, private_key):
        crypto.sign(f'amount: {self.amount}, sender: {self.sender}, recipient: {self.recipient},', private_key)

    # todo verify if address has enough balance
    def is_valid(self):
        return crypto.verify((self.amount, self.recipient, self.sender), self.signature, self.sender)
