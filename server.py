import socket
import pickle
from select import select


class Server:
    def __init__(self):
        self.to_monitor = []
        self.levels = [
            [
            "111111111111111111111111111111",
            "120000010000000100000000100001",
            "111111010111110101111110111101",
            "100000010100000000000010000001",
            "101111010101111101011011111101",
            "101000010101000001000000000001",
            "101011110100010101011010110101",
            "100010000001000101000010100101",
            "111010110101111101111110101101",
            "101010110100000000100000000001",
            "101010110101111110111101011101",
            "101000000100000010000001010001",
            "101111101111111010111101010101",
            "100000000000000010000000000031",
            "111111111111111111111111111111"
            ]
        ]
        self.players_now = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 5001))
        self.socket.listen(2)

    def accept_connection(self, server_socket):
        client_scoket, addr = server_socket.accept()
        self.players_now += 1
        msg = 'id ' + str(self.players_now)
        client_scoket.send(msg.encode())
        self.to_monitor.append(client_scoket)


    def handle(self, req):
        pass

    def send_command(self, client_socket):
        request = client_socket.recv(4096)
        if request:
            response = self.handle(request)
            client_socket.send(response.encode())
        else:
            client_socket.close()
            self.to_monitor.remove(client_socket)
    

    def event_loop(self):
        while True:
            ready_to_read, _, _ = select(self.to_monitor, [], [])

            for s in ready_to_read:
                if s is self.socket:
                    self.accept_connection(s)
                else:
                    self.send_command(s)
    

    def start(self):
        self.to_monitor.append(self.socket)
        self.event_loop()


if __name__ == "__main__":
    Server().start()