import socket
import threading
import random
import time

class BridgeServer:
    def __init__(self, host='localhost', port=65432):
        self.host = host
        self.port = port
        self.clients = []
        self.bridge_lock = threading.Lock()
        self.bridge_state = 'Free'

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server started at {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()

    def handle_client(self, conn, addr):
        print("Connected by {addr}")
        self.clients.append(conn)
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode()
                if command == 'REQUEST_CROSS':
                    self.handle_cross_request(conn)
        finally:
            print(f"Disconnected {addr}")
            self.clients.remove(conn)
            conn.close()

    def handle_cross_request(self, conn):
        with self.bridge_lock:
            self.bridge_state = 'Occupied'
            self.broadcast_state()
            time.sleep(random.randint(1, 5))  # Simulate crossing time
            self.bridge_state = 'Free'
            self.broadcast_state()

    def broadcast_state(self):
        state_message = "BRIDGE_STATE:{self.bridge_state}"
        for client in self.clients:
            client.sendall(state_message.encode())

if __name__ == "__main__":
    server = BridgeServer()
    server.start_server()
