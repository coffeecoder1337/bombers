import pickle
import socket


class Server:
    def __init__(self, port = 5005): # 5005
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', port))
        self.games = 0
        self.clients = dict()

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

                if network_object.event == "connect":
                    try:
                        last_game_length = len(self.clients[list(self.clients.keys())[-1]])
                    except:
                        last_game_length = 0
                    if last_game_length in [0, 2]:
                        self.games += 1
                        self.clients[self.games] = []
                        self.clients[self.games].append(adress)
                        network_object.symbol = "#"
                    else:
                        self.clients[self.games].append(adress)
                        network_object.symbol = "$"
                    network_object.game_id = self.games
                    network_object.send_to_client(self.server_socket, adress)
                    
                else:
                    for client in self.clients[network_object.game_id]:
                        if adress != client:
                            network_object.send_to_client(self.server_socket, client)
                if network_object.event == "left":
                    clients = self.clients[network_object.game_id]
                    clients.remove(adress)
                    if len(clients) == 0:
                        self.clients.pop(network_object.game_id)
                print(self.clients)

    def run(self):
        self.loop()
        self.server_socket.close()


server = Server()
server.run()
