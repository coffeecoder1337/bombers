import pickle

class NetworkObject:
    def __init__(self, event=None, coords=None, hp=None, game_id=None, symbol=None):
        self.event = event
        self.coords = coords
        self.hp = hp
        self.game_id = game_id
        self.symbol = symbol


    def send_to_server(self, client_socket):
        client_socket.send(pickle.dumps(self))


    def send_to_client(self, server_socket, addr):
        server_socket.sendto(pickle.dumps(self), addr)
