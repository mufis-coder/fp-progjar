import socket
import select
import sys
import threading
import pickle
import time
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
# ip_address = ''
# port = 5555
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
clients_login = set()

def data_send(player, act, val=None):
    data_dict = {"Player":player, "Action":act, "Value":val}
    data = pickle.dumps(data_dict)
    return data

def clientthread(conn, addr):
    global game_datas
    while True:
        try:
            message = conn.recv(2048)
            if message:
                if message:
                    msg_ori = pickle.loads(message)
                    if(msg_ori['Action'] == "Add Pipe"):
                        broadcast(data_send(msg_ori['Player'], "Height Pipe", random.randrange(50, 450)))
                    elif(msg_ori['Action'] == "Start"):
                        clients_login.add(msg_ori['Player'])
                        if(len(clients_login)==2):
                            time.sleep(5)
                            broadcast(data_send("Player1", "Start"))
                            broadcast(data_send("Player2", "Start"))
                    elif(msg_ori['Action'] == "End"):
                        clients_login.remove(msg_ori['Player'])
                    else:
                        broadcast(message)
                    print("print u: " + str(msg_ori))
                    print("Client login: " + str(clients_login))
            else:
                remove(conn)
        except:
            continue

def broadcast(message):
    for client in list_of_clients:
        try:
            client.send(message)
        except:
            client.close()
            remove(client)

def remove(connection):
    for key, value in list_of_clients.items():
         if connection == value:
             list_of_clients = list_of_clients.pop(key)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()