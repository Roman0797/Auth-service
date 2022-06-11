import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', 9090))
sock.listen(5)
sock.setblocking(False)

while True:
    try:
        conn, addr = sock.accept()
        print('connected:', addr)
    except socket.error:
        print('нет клиента')
    except KeyboardInterrupt:
        break
    else:
        conn.setblocking(True)
        data = conn.recv(1024)
        data = data.decode()
        data = data.upper()
        conn.send(data.encode())
        print(data)
        conn.close()
