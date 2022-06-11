import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 9090))
text = input('Введите имя')
b = bytes(text, encoding='utf-8')
sock.send(b)

data = sock.recv(1024)
sock.close()
data = data.decode()
print(data)