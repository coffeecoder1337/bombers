import pickle
import socket


class Server:
    def __init__(self, port): # 5005
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', port))





# close socket...
