import socket
import pickle
import random
from select import select


class Server:
    def __init__(self):
        self.to_monitor = []
        self.levels = [
            {
                'blue_spawn_coords': [30, 30],
                'red_spawn_coords': [840, 390],
                'level': [
                    "111111111111111111111111111111",
                    "100000010000000100000000100001",
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
                    "100000000000000010000000000001",
                    "111111111111111111111111111111"
                ]
            }
        ]
        self.players = 0
        self.games = 0
        self.prev_client = 0
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 5001))
        self.socket.listen(2)

    def accept_connection(self, server_socket):
        client_scoket, addr = server_socket.accept()
        print(client_scoket)
        level = random.randint(0, len(self.levels) - 1)
        data = {
            'type': 'connected',
            'id': self.players,
            'level': self.levels[level]['level']
        }

        if self.players % 2 == 0:
            data['spawn_coords'] = self.levels[level]['blue_spawn_coords']
            data['enemy_spawn_coords'] = self.levels[level]['red_spawn_coords']
            data['pause'] = True
            self.prev_client = client_scoket
        else:
            data['spawn_coords'] = self.levels[level]['red_spawn_coords']
            data['enemy_spawn_coords'] = self.levels[level]['blue_spawn_coords']
            data['pause'] = False
            unpause_data = {
                'type': 'unpause'
            }
            print(self.prev_client)
            self.prev_client.send(pickle.dumps(unpause_data))
            self.games += 1

        client_scoket.send(pickle.dumps(data))
        self.clients.append(client_scoket)
        self.to_monitor.append(client_scoket)
        self.players += 1

    def resend(self, client_socket):
        data = pickle.loads(client_socket.recv(4096))
        if data:
            if data['id'] % 2 == 0:
                client = data['id'] + 1
            else:
                client = data['id'] - 1
            self.clients[client].send(pickle.dumps(data))
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
                    self.resend(s)
    

    def start(self):
        self.to_monitor.append(self.socket)
        self.event_loop()


if __name__ == "__main__":
    Server().start()