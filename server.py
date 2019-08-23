import socket
from select import select


class Server:
    def __init__(self):
        self.to_monitor = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('localhost', 5001))
        self.socket.listen(2)

    def accept_connection(self, server_socket):
        client_scoket, addr = server_socket.accept()
        self.to_monitor.append(client_scoket)


    def handle(self, req):
        req = req.decode().split()
        print(req)
        if req[0] == 'get':
            if req[1] == 'coords':
                return '100 50'.encode()


    def send_command(self, client_socket):
        request = client_socket.recv(4096)
        if request:
            response = self.handle(request)
            client_socket.send(response)
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