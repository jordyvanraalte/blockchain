import unittest
import os
from blockchain.structure.wallet import Wallet
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption



class TestWallet(unittest.TestCase):
    def test_address(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        addr = wallet1.address
        self.assertIsNotNone(addr)

    def test_write_keys(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet1.write_keys()

        self.assertTrue(os.path.isfile('.pem') and os.path.isfile('public.pem'))

        os.remove('.pem')
        os.remove('public.pem')

    def test_read_keys(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet1.write_keys()

        wallet2 = Wallet()
        wallet2.read_keys()

        pem_wallet_1 = wallet1.private_key.private_bytes(encoding=Encoding.PEM,
                                                         format=PrivateFormat.PKCS8,
                                                         encryption_algorithm=NoEncryption())
        pem_wallet_2 = wallet1.private_key.private_bytes(encoding=Encoding.PEM,
                                                         format=PrivateFormat.PKCS8,
                                                         encryption_algorithm=NoEncryption())

        self.assertTrue(pem_wallet_1 == pem_wallet_2)

        os.remove('.pem')
        os.remove('public.pem')

    def test_valid_password(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet1.write_keys(password="password")

        wallet2 = Wallet()
        wallet2.read_keys(password="password")

        pem_wallet_1 = wallet1.private_key.private_bytes(encoding=Encoding.PEM,
                                                         format=PrivateFormat.PKCS8,
                                                         encryption_algorithm=NoEncryption())
        pem_wallet_2 = wallet1.private_key.private_bytes(encoding=Encoding.PEM,
                                                         format=PrivateFormat.PKCS8,
                                                         encryption_algorithm=NoEncryption())

        self.assertTrue(pem_wallet_1 == pem_wallet_2)

        os.remove('.pem')
        os.remove('public.pem')

    def test_non_valid_password(self):
        wallet1 = Wallet()
        wallet1.create_keys()
        wallet1.write_keys(password="password1")

        wallet2 = Wallet()
        with self.assertRaises(ValueError, msg='ValueError: Bad decrypt. Incorrect password?'):
            wallet2.read_keys(password="password2")


        os.remove('.pem')
        os.remove('public.pem')
