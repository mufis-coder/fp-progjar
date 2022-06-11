import socket
import select
import sys
import threading
import pickle
import time
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# ip_address = '127.0.0.1'
# port = 8081
ip_address = ''
port = 5555
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
                    #Handle when user want "Add Pipe"
                    if(msg_ori['Action'] == 3):
                        broadcast(data_send(msg_ori['Player'], 4, random.randrange(50, 450)))
                    #Handle when user want "Start"
                    elif(msg_ori['Action'] == 1):
                        clients_login.add(msg_ori['Player'])
                        if(len(clients_login)==2):
                            sec = 0
                            while True:
                                time.sleep(0.9)
                                sec += 1
                                broadcast(data_send(0, 0, sec))
                                broadcast(data_send(1, 0, sec))
                                if sec >= 5:
                                    break
                            broadcast(data_send(0, 1))
                            broadcast(data_send(1, 1))
                    #Handle when user want "End"
                    elif(msg_ori['Action'] == -1):
                        clients_login.remove(msg_ori['Player'])
                    #Handle when user want "Jump", "Bird Height"
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