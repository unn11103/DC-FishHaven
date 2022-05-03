import socket
import threading
import sys
import time
# sys.path.append('../src')
from FishData import FishData
from PondData import PondData
from Payload import Payload
import pickle
from queue import Queue

IP = socket.gethostbyname(socket.gethostname())
PORT = 8016
ADDR = (IP, PORT)
MSG_SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

all_connections = {}

payload = Payload() #Initialize payload

def handle_pond(connection, address):
    print(f"New pond connected from : {address}")

    connected = True
    while connected:
        message = connection.recv(MSG_SIZE)
        #separate message type

        msg = pickle.loads(message)
        # print(f"{address} : {msg}")
        # print(all_connections)
        if msg.action == DISCONNECT_MSG:
            connected = False
            all_connections.pop(address)
            for addr, conn in all_connections.items():
                # conn.send(f"{address} disconnected.".encode(FORMAT))
                print("-------------------------",msg.action)
                print(msg.data)
                temp = Payload()
                temp.action = DISCONNECT_MSG
                temp.data = msg.data
                conn.send(pickle.dumps(temp))

        else:
            for addr, conn in all_connections.items():
                print(msg)
                print("The Pond has sent")
                
                conn.send(pickle.dumps(msg))

    connection.close()

if __name__ == "__main__":
    print("Starting vivisystem...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(100)
    print(f"Vivisystem is listening on {IP}:{PORT}")

    while True:
        add, con = server.accept()
        if (type(add) == tuple):
            clientAddress = add
            clientConnection = con
        else:
            clientAddress = con
            clientConnection = add

        all_connections[clientAddress] = clientConnection

        pond_handler = threading.Thread(target=handle_pond, args=(clientConnection, clientAddress,))
        pond_handler.start()
        print(f"Ponds in the vivisystem: {threading.activeCount() - 1} {clientConnection} {clientAddress}")
