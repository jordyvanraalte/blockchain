import base64

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def new_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def sign(message, private_key):
    message = bytes(str(message), 'utf-8')
    return private_key.sign(message,
                            padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            hashes.SHA256()
                            )


def verify(message, signature, public_key):
    message = bytes(str(message), 'utf-8')
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def write_private_key(path, private_key, password=None):
    if password:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(password.encode('utf-8'))
        )
    else:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    f = open(path, 'wb')
    f.write(pem)
    f.close()


def write_public_key(path, public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    f = open(path, 'wb')
    f.write(pem)
    f.close()


def read_private_key(path, password=None):
    if password:
        with open(path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password.encode('utf-8'),
            )
            return private_key
    else:
        with open(path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
            return private_key


def read_public_key(path):
    with open(path, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read())
        return public_key


def encode_addr(public_key):
    base64_value = base64.b64encode(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PublicFormat.SubjectPublicKeyInfo))
    # decode to utf-8 string
    return base64_value.decode('utf-8')


def decode_addr(addr):
    base_64_bytes = addr.encode('utf-8')
    pem = base64.b64decode(base_64_bytes)
    public_key = serialization.load_pem_public_key(pem)
    return public_key


def base64_encode_bytes(bytes):
    base64_value = base64.b64encode(bytes).decode('utf-8')
    return base64_value


def base64_decode_bytes(string):
    bytes_value = base64.b64decode(string.encode('utf-8'))
    return bytes_value
