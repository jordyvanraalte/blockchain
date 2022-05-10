from flask import Flask


class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.app = Flask(__name__)

    def start(self):
        self.app.run(host=self.addr, port=self.port)
