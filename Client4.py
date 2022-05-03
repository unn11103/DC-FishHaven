import socket
import threading
import sys
import time
import random
from queue import Queue

# sys.path.append('../src')
from FishData import FishData
from PondData import PondData
from Payload import Payload

import pickle
IP = socket.gethostbyname(socket.gethostname())
PORT = 8003
ADDR = (IP, PORT)
MSG_SIZE = 4096
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


class Client:
    def __init__(self,pond):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = IP
        self.port = PORT
        self.addr = ADDR
        self.connected = True
        self.other_ponds = {}
        self.msg = self.connect()
        self.payload = Payload()
        self.pond = pond
        self.messageQ = []

    def get_msg(self):
        while True:
            time.sleep(0.5)
            msg = pickle.loads(self.client.recv(MSG_SIZE))
            if(msg):
                self.messageQ.append(msg)
                self.handle_msg(msg)
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Client connected ")
            return "Connected"
        except:
            print("Can not connect to the server")

    def send_pond(self):
        try:
            while True:
                time.sleep(2)
                self.payload.action = "SEND"
                self.payload.data = self.pond
                #print("Client send :",self.pond)
                self.client.send(pickle.dumps(self.payload))
                #msg =  pickle.loads(self.client.recv(MSG_SIZE))
                #return self.handle_msg(msg)

        except socket.error as e:
            print(e)

    def migrate_fish(self, fishData , destination):
        ### Migration takes a special object for the payload to pickup : The destination pond's name 
        try:

            migration = {
                "destination" : destination,
                "fish" : fishData
            }
            self.payload.action = "MIGRATE"
            self.payload.data = migration

            self.client.send(pickle.dumps(self.payload))
            print("=======MIGRATED=======")            
            ### Handle our fish in the pond
            # // TO BE IMPLEMENTED

            msg =  pickle.loads(self.client.recv(MSG_SIZE))
            return self.handle_msg(msg)
            

            # print("Client send :",pond)
            # next_pond = random.random_choice(self.other_ponds.keys())
            # self.client.send("MIGRATE FROM sick_salmon TO "+ next_pond + " " + pickle.dumps(fishData))
            # msg =  pickle.loads(self.client.recv(MSG_SIZE))
            # return self.handle_msg(msg)
        except socket.error as e:
            print(e)
    
    def disconnect(self) :
        try:
            self.payload.action = DISCONNECT_MSG
            print("Disconnecting...")
            self.client.send(pickle.dumps(self.payload))
            return self.client.recv(MSG_SIZE)

        except socket.error as e:
            print(e)

    def handle_msg(self, msg):
        msg_action = msg.action
        msg_object = msg.data
        #print(self.messageQ)

        if(msg_action == "SEND") :
            self.other_ponds[msg_object.pondName] = msg_object #Update in the dict key = pondname, values = <PondData>
            print(self.other_ponds)
            return msg
        
        if(msg_action == "MIGRATE"):
            if(self.pond.pondName == msg_object["destination"]):
                print("=======RECIEVED MIGRATION=======")
                self.pond.addFish(msg_object["fish"])
                print(self.pond.fishes)
                print("================================")
        
        else:
            pass
        # if msg[:7] == "MIGRATE":
        #     pass
        # elif msg[:4] == "JOIN":
        #     pass
        # elif msg[:11] == "DISCONNECT":
        #     pass
        # else:
        #     print(f"Vivisystem : {msg}")
        #     return msg

if __name__ == "__main__":

    f1 = FishData("Sick Salmon","123456")
    f2 = FishData("Fish2","123456")
    p = PondData("final")
    p.addFish(f1)
    p.addFish(f2)
    connected = True
    c = Client(p)
    msg_handler = threading.Thread(target=c.get_msg)   
    msg_handler.start() 
    send_handler = threading.Thread(target=c.send_pond)
    send_handler.start()
    # while(connected) :

    #     #c.migrate_fish(f1,"sick salmon")
    #     #c.migrate_fish(f2,"sick salmon")


