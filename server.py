import socket
from select import select


'''
set 30 40 - изменить текущие координаты
get - получить текущие координаты
'''


class Server:
    def __init__(self):
        self.to_monitor = []
        self.players_now = 0
        self.data = {
            "0": {
                "coords": "30 30"
            },
            "1": {
                "coords": "870 420"
            }
        }
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('', 5001))
        self.socket.listen(2)

    def accept_connection(self, server_socket):
        client_scoket, addr = server_socket.accept()
        msg = 'id ' + str(self.players_now)
        client_scoket.send(msg.encode())
        self.players_now += 1
        self.to_monitor.append(client_scoket)


    def handle(self, req):
        req = req.decode().split()
        if req[1] == 'set':
            if req[0] == "0":
                self.data["0"]['coords'] = req[2] + ' ' + req[3]
                return self.data["1"]['coords']
            if req[0] == "1":
                self.data["1"]['coords'] = req[2] + ' ' + req[3]
                return self.data["0"]['coords']

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