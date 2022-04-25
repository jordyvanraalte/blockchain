from blockchain.utils import crypto


class Wallet:

    def __init__(self):
        private, public = crypto.new_keys()
        self.private_key = private
        self.public_key = public

    def create_keys(self):
        private, public = crypto.new_keys()
        self.private_key = private
        self.public_key = public

    # noinspection PyTypeChecker
    def read_keys(self, private_key_path=".pem", public_key_path="public.pem", password=None):
        private = crypto.read_private_key(private_key_path, password)
        public = crypto.read_public_key(public_key_path)
        self.private_key = private
        self.public_key = public

    def write_keys(self, private_key_path=".pem", public_key_path="public.pem", password=None):
        crypto.write_private_key(private_key_path, self.private_key, password)
        crypto.write_public_key(public_key_path, self.public_key)

    @property
    def address(self):
        return crypto.encode_addr(self.public_key)
