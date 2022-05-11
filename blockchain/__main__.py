import argparse
from blockchain.utils import crypto
from blockchain.app import run


def main(addr, port, debug):
    run(addr, port, None, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--addr', '-a', type=str, help='Defines the address of the application.', default='0.0.0.0')
    parser.add_argument('--port', '-p', type=int, help='Defines the port of the application.', default=50000)
    parser.add_argument('--debug', '-d', action="store_true", help='', default=False)
    parser.add_argument('--private_key', '-pk', action="store", type=str,
                        help='path of private key if private key provided')
    parser.add_argument('--public_key', '-pubk', action="store", type=str,
                        help='path of public key if public key provided')
    parser.add_argument('--generate_keys', '-gen_keys', action="store_true", help='', default=False)

    args = parser.parse_args()

    if args.generate_keys:
        private, public = crypto.new_keys()
        crypto.write_private_key('.pem', private)
        crypto.write_public_key('public.pem', public)
        print(f"New keys have been generated and saved. Public address of key pair is: {crypto.encode_addr(public)}")
    else:
        main(args.addr, args.port, args.debug)


