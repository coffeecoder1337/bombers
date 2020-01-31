import pickle
import socket


class Server:
    def __init__(self, port = 5005): # 5005
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', port))
        self.games = 0
        self.clients = []

    def loop(self):
        while True:
            try:
                data = self.server_socket.recvfrom(2048)
                print(data)
            except Exception as e:
                print(e)
                self.clients.clear()
            else:
                network_object = pickle.loads(data[0])
                adress = data[1]
                if adress not in self.clients:
                    self.clients.append(adress)
                    if len(self.clients) % 2 == 1:
                        self.games += 1
                        network_object.symbol = "#"
                    else:
                        network_object.symbol = "$"
                    network_object.game_id = self.games
                    network_object.send_to_client(self.server_socket, adress)
                    
                else:
                    for client in self.clients:
                        if adress != client:
                            network_object.send_to_client(self.server_socket, client)
                if network_object.event == "left":
                    self.clients.clear()

    def run(self):
        self.loop()
        self.server_socket.close()


server = Server()
server.run()
