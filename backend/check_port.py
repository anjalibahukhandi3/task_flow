import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex(('127.0.0.1', 8000))
with open('port_check.txt', 'w') as f:
    if result == 0:
        f.write("Port 8000 is OPEN")
    else:
        f.write("Port 8000 is CLOSED")
