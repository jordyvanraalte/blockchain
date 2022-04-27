import uuid

from blockchain.utils import crypto


class Transaction:
    def __init__(self):
        self.id = uuid.uuid4()
        self.inputs = []
        self.outputs = []
        self.signatures = []
        self.multi_signing_addresses = []

    def __repr__(self):
        return f"id: {self.id},  inputs: {self.inputs}, outputs: {self.outputs}, signatures: {self.signatures}, multi_signatures: {self.multi_signing_addresses}"

    def add_input(self, sender, amount):
        self.inputs.append((sender, amount))

    def add_output(self, recipient, amount):
        self.outputs.append((recipient, amount))

    def add_multi_signing_address(self, addr):
        self.multi_signing_addresses.append(addr)

    def sign(self, private_key):
        self.signatures.append(crypto.sign(self.gather_signing_data(), private_key))

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


class CoinbaseTransaction(Transaction):
    # coinbase transaction is always valid
    def is_valid(self):
        return True
