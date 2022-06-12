import pickle
import sys

def data_send(player, act, val=None):
    data_dict = {"Player":player, "Action":act, "Value":val}
    data = pickle.dumps(data_dict)
    return data

def send_msg(sock, data):
    sock.send(data)
    sys.stdout.flush()

def recv_msg(sock):
    try:
        data = sock.recv(2048)
        data_pick = pickle.loads(data)
        # print("Message from server: " + str(data_pick))
        return data_pick
    except:
        # print("Exception Occured!")
        pass