import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 5001))
s.send('get coords'.encode())
data = s.recv(4096)
s.close()
coords = data.decode().split()
coords[0], coords[1] = int(coords[0]), int(coords[1])
print(coords)