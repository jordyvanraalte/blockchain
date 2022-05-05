import socket
import threading
import uuid
import time
import json
from struct import unpack, pack

MAX_INBOUND_CONNECTIONS = 125
MAX_OUTBOUND_CONNECTIONS = 10


# https://github.com/macsnoeren/python-p2p-network
class PeerConnection(threading.Thread):
    def __init__(self, id, addr, port, main_node, sock):
        super().__init__()
        self.id = id
        self.addr = addr
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()
        self.sock.settimeout(10.0)

    def send(self, data, encoding_type='utf-8'):
        if isinstance(data, str):
            encoded_data = data.encode(encoding_type)
            length = pack('>Q', len(encoded_data))
            self.sock.sendall(length)
            self.sock.sendall(encoded_data)
        elif isinstance(data, dict):
            json_data = json.dumps(data)
            encoded_json_data = json_data.encode(encoding_type)
            length = pack('>Q', len(encoded_json_data))
            self.sock.sendall(length)
            self.sock.sendall(encoded_json_data)
        elif isinstance(data, bytes):
            length = pack('>Q', len(data))
            self.sock.sendall(length)
            self.sock.sendall(data)
        else:
            raise Exception("Datatype of transmission was not valid, use str, dict or bytes.")

    def stop(self):
        self.terminate_flag.set()

    @staticmethod
    def parse_packet(packet):
        try:
            packet_decoded = packet.decode('utf-8')
            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                return packet_decoded

        except UnicodeDecodeError:
            return packet

    def run(self):
        while not self.terminate_flag.is_set():
            try:
                # get length of upcoming package
                bs = self.sock.recv(8)
                if len(bs) > 0:
                    (length,) = unpack('>Q', bs)
                    buffer = b''
                    # while the length of the buffer is smaller than the length of the package
                    while len(buffer) < length:
                        to_read = length - len(buffer)
                        buffer += self.sock.recv(4096 if to_read > 4096 else to_read)

                    packet = PeerConnection.parse_packet(buffer)
                    self.main_node.node_message(self, packet)
            except socket.timeout:
                # todo add debug option for timeout.
                # print("Socket timeout, waiting for new packets again.")
                pass
            except Exception as e:
                print(e)
                raise e
                self.terminate_flag.set()

        self.main_node.node_disconnected(self)
        self.sock.settimeout(None)
        self.sock.close()
        self.main_node.debug_print(f"PeerConnection: {self.addr}:{self.port} stopped")

    def __repr__(self):
        return f'Peer connection: {self.id}, {self.addr}:{self.port} <-> {self.main_node}'


class Node(threading.Thread):
    def __init__(self, addr, port, callback=None, debug=False):
        super(Node, self).__init__()

        self.id = str(uuid.uuid4())
        # server address
        self.addr = addr
        # server port
        self.port = port

        # peers
        self.inbound_peers = []
        self.outbound_peers = []

        self.sock = socket.socket(socket.AF_INET)
        self.init_server()

        self.terminate_flag = threading.Event()

        self.callback = callback

        self.debug = debug

    def init_server(self):
        self.sock.bind((self.addr, self.port))
        self.sock.settimeout(10.0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.listen(1)
        print(f'Node server started on {self.addr}:{self.port}')

    def debug_print(self, message):
        if self.debug:
            print(f'DEBUG: {self.id}: {message}')

    def broadcast(self, data):
        for node in self.inbound_peers:
            node.send(data)

        for node in self.outbound_peers:
            node.send(data)

        self.debug_print(f"Broadcasting: {data}")

    def connect(self, addr, port):
        if addr == self.addr and port == self.port:
            self.debug_print(f"Can't connect with own node {addr}:{port}")
            return False

        if any(node.addr == addr and node.port == port for node in self.outbound_peers):
            self.debug_print(f"Connection with node {addr}:{port} already exists")
            return True

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.debug_print(f"Connecting with node {addr}:{port}")
            sock.connect((addr, port))

            # identification
            sock.send((str(self.id) + ":" + str(self.port)).encode('utf-8'))
            connected_node_id = sock.recv(4096).decode('utf-8')

            if str(self.id) == str(connected_node_id):
                self.debug_print(f"Can't connect with yourself {addr}:{port}")
                sock.send("CLOSING: Already having a connection together".encode('utf-8'))
                sock.close()
                return True

            if any(node.id == connected_node_id and node.addr == addr for node in self.outbound_peers):
                self.debug_print(f"Already connected {addr}:{port}")
                sock.send("CLOSING: Already having a connection together".encode('utf-8'))
                sock.close()
                return True

            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            peer_connection = self.create_peer_connection(connected_node_id, addr, port, sock)
            peer_connection.start()

            self.outbound_peers.append(peer_connection)
            self.outbound_peer_connected(peer_connection)
            return True
        except Exception as e:
            print(e)
            raise e
            return False

    def send(self, node, data):
        if any(str(node.id) == str(out_n.id) for out_n in self.inbound_peers) or any(
                str(node.id) == str(out_n.id) for out_n in self.outbound_peers):
            node.send(data)
        else:
            self.debug_print(f"Data has not been send to: {node}")

    def disconnect_with_node(self, node):
        if node in self.outbound_peers:
            self.node_disconnect_with_outbound_peer(node)
            node.stop()

    def stop(self):
        self.node_request_to_stop()
        self.terminate_flag.set()

    def run(self) -> None:
        while not self.terminate_flag.is_set():
            try:
                self.debug_print("Node: Wait for incoming connection")
                conn, client_address = self.sock.accept()
                self.debug_print(
                    f"connection accepted from {client_address}. Total connections: {len(self.inbound_peers) + 1}")

                if len(self.inbound_peers) < MAX_OUTBOUND_CONNECTIONS:
                    address = client_address[0]
                    connected_node_id = conn.recv(4096).decode('utf-8')
                    (connected_node_id, connected_node_port) = connected_node_id.split(':')
                    conn.send(str(self.id).encode('utf-8'))
                    peer_connection = self.create_peer_connection(connected_node_id, address, connected_node_port, conn)
                    peer_connection.start()
                    self.inbound_node_connected(peer_connection)
                    self.inbound_peers.append(peer_connection)
                else:
                    conn.close()
            except socket.timeout:
                # print(f"Socket timeout from node")
                pass
            except Exception as e:
                raise e

            time.sleep(1)

        print("Node stopping...")
        for p in self.inbound_peers:
            p.stop()

        for p in self.outbound_peers:
            p.stop()

        time.sleep(1)

        for p in self.inbound_peers:
            p.join()

        for p in self.outbound_peers:
            p.join()

        self.sock.settimeout(None)
        self.sock.close()
        print("Node stopped")

    def create_peer_connection(self, id, addr, port, conn):
        return PeerConnection(id, addr, port, self, conn)

    def inbound_node_connected(self, node):
        self.debug_print("inbound_peer_connected: " + node.id)
        if self.callback is not None:
            self.callback("inbound_peer_connected", self, node, {})

    def outbound_peer_connected(self, node):
        self.debug_print("outbound_peer_connected: " + node.id)
        if self.callback is not None:
            self.callback("outbound_peer_connected", self, node, {})

    def node_disconnected(self, node):
        self.debug_print("node_disconnected: " + node.id)

        if node in self.inbound_peers:
            del self.inbound_peers[self.inbound_peers.index(node)]
            self.inbound_node_disconnected(node)

        if node in self.outbound_peers:
            del self.outbound_peers[self.outbound_peers.index(node)]
            self.outbound_node_disconnected(node)

    def inbound_node_disconnected(self, node):
        self.debug_print("inbound_node_disconnected: " + node.id)
        if self.callback is not None:
            self.callback("inbound_node_disconnected", self, node, {})

    def outbound_node_disconnected(self, node):
        self.debug_print("outbound_node_disconnected: " + node.id)
        if self.callback is not None:
            self.callback("outbound_node_disconnected", self, node, {})

    def node_message(self, node, data):
        self.debug_print("node_message: " + node.id + ": " + str(data))
        if self.callback is not None:
            self.callback("node_message", self, node, data)

    def node_disconnect_with_outbound_peer(self, node):
        self.debug_print("node wants to disconnect with oher outbound peeer: " + node.id)
        if self.callback is not None:
            self.callback("node_disconnect_with_outbound_node", self, node, {})

    def node_request_to_stop(self):
        self.debug_print("node is requested to stop!")
        if self.callback is not None:
            self.callback("node_request_to_stop", self, {}, {})

    def __repr__(self):
        return f'Node: {self.id}, {self.addr}:{self.port}'


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    node1 = Node('0.0.0.0', port, debug=True)
    node1.start()

    node2 = Node('0.0.0.0', 50432, debug=True)
    node2.start()
    node2.connect('0.0.0.0', port)

    node3 = Node('0.0.0.0', 33423, debug=True)
    node3.start()
    node3.connect('0.0.0.0', port)

    node1.broadcast("hi")
    time.sleep(30)
    node1.broadcast("hi")
