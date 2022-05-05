import uuid
import copy
import jsons

from blockchain.utils import crypto


class Transaction:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.inputs = []
        self.outputs = []
        self.signatures = []
        self.multi_signing_addresses = []

    def __repr__(self):
        return f"id: {self.id}, inputs: {self.inputs}, outputs: {self.outputs}, signatures: {self.signatures}. multi_signing_addresses: {self.multi_signing_addresses}"

    def __eq__(self, other):
        return self.id == other.id and self.inputs == other.inputs and self.outputs == other.outputs and self.signatures == other.signatures and self.multi_signing_addresses == other.multi_signing_addresses

    def add_input(self, sender, amount):
        self.inputs.append((sender, amount))

    def add_output(self, recipient, amount):
        self.outputs.append((recipient, amount))

    def add_multi_signing_address(self, addr):
        self.multi_signing_addresses.append(addr)

    def sign(self, private_key):
        signature_bytes = crypto.sign(self.gather_signing_data(), private_key)
        self.signatures.append(signature_bytes)

    def total_input_amount(self):
        return sum(amount for sender, amount in self.inputs)

    def total_output_amount(self):
        return sum(amount for recipient, amount in self.outputs)

    def gather_signing_data(self):
        return self.inputs, self.outputs, self.multi_signing_addresses

    # todo verify if address has enough balance
    def is_valid(self):
        data = self.gather_signing_data()
        # total inputs need to be greater or equal
        if self.total_input_amount() < self.total_output_amount():
            return False

        return self.__validate_inputs(data) and self.__validate_outputs() and self.__validate_multi_signing_addresses(
            data)

    def __validate_inputs(self, data):
        for sender, amount in self.inputs:
            found = False
            # if input is negative transaction is not valid
            if amount < 0:
                return False

            # validating if a signature exist with the corresponding input address.
            for signature in self.signatures:
                if crypto.verify(data, signature, crypto.decode_addr(sender)):
                    found = True

            if not found:
                return False
        return True

    def __validate_outputs(self):
        # check if output has not any transaction amount below zero.
        return not any([amount < 0 for recipient, amount in self.outputs])

    def __validate_multi_signing_addresses(self, data):
        for addr in self.multi_signing_addresses:
            found = False
            for signature in self.signatures:
                if crypto.verify(data, signature, crypto.decode_addr(addr)):
                    found = True

            if not found:
                return False

        return True

    @staticmethod
    def encode(t):
        def to_dict(transaction):
            return {"address": transaction[0], 'amount': transaction[1]}

        t = copy.copy(t)
        t.inputs = list(map(lambda i: to_dict(i), t.inputs))
        t.outputs = list(map(lambda o: to_dict(o), t.outputs))
        t.signatures = list(map(lambda s: crypto.base64_encode_bytes(s), t.signatures))
        # returns a copy since memory id will be the same, todo change later
        return t

    @staticmethod
    def decode(t):
        def to_tuple(transaction):
            return transaction['address'], transaction['amount']

        if type(t) is dict:
            if len(t['inputs']) == 0:
                t = jsons.loads(jsons.dumps(t), CoinbaseTransaction)
            else:
                t = jsons.loads(jsons.dumps(t), Transaction)

        t = copy.copy(t)
        t.inputs = list(map(lambda i: to_tuple(i), t.inputs))
        t.outputs = list(map(lambda o: to_tuple(o), t.outputs))
        t.signatures = list(map(lambda s: crypto.base64_decode_bytes(s), t.signatures))
        # returns a copy since memory id will be the same, todo change later
        return t


class CoinbaseTransaction(Transaction):
    # coinbase transaction is always valid
    def is_valid(self):
        return True
