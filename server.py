import asyncio
import pickle
import socket


class Server:
    def __init__(self, port = 5005): # 5005
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', port))
        self.clients = []
        self.counter = 0

    def loop(self):
        while True:
            data = self.server_socket.recvfrom(1024)
            message = data[0].decode()
            adress = data[1]
            if adress not in self.clients:
                self.clients.append(adress)
                if len(self.clients) % 2 == 1:
                    msg = "#"
                else:
                    msg = "$"
                self.server_socket.sendto(msg.encode(), adress)
            else:
                for client in self.clients:
                    if adress != client:
                        self.server_socket.sendto(message.encode(), client)

    def run(self):
        self.loop()
        self.server_socket.close()


server = Server()
server.run()
