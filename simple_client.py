import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5001))
s.send('get coords character start'.encode())
data = s.recv(4096)
s.close()
print(data.decode())