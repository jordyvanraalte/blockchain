from blockchain.utils import crypto


class Wallet:
    # todo add address generation based on bitcoin protocol.

    def __init__(self):
        private, public = crypto.new_keys()
        self.private_key = private
        self.public_key = public

    # noinspection PyTypeChecker
    def load_keys(self, private_key_path="private.pem", public_key_path="public.pem", password=None):
        private = crypto.load_pem_private_key(private_key_path, password)
        public = crypto.load_pem_public_key(public_key_path)
        self.private_key = private
        self.public_key = public

    def write_keys(self, private_key_path=".pem", public_key_path="public.pem", password=None):
        crypto.write_private_key(private_key_path, self.private_key, password)
        crypto.write_public_key(public_key_path, self.public_key)