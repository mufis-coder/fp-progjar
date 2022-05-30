import socket
import select
import sys
import threading
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8081
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
client_types = {}

def clientthread(conn, addr):
    global game_datas
    while True:
        try:
            message = conn.recv(2048)
            if message:
                if message:
                    msg_ori = pickle.loads(message)
                    print("print u: " + str(msg_ori))
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in list_of_clients.values():
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def remove(connection):
    for key, value in list_of_clients.items():
         if connection == value:
             list_of_clients = list_of_clients.pop(key)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    if(len(list_of_clients)==2):
        pass
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
