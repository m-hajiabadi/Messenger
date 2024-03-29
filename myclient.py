import socket
import threading
import sys
import time

class Client(threading.Thread): # Client object is type thread so that it can run simultaniously with the server
    def __init__(self, chatApp): # Initialize with a reference to the Chat App
        super(Client, self).__init__()
        self.chatApp = chatApp
        self.isConnected = False # Connection status

    # Start method called by threading module
    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create new socket
        self.socket.settimeout(5)
    
    def conn(self, args):
        if self.chatApp.nickname == "": # Check if a nickname is set and return False if not
            print("nickNotSet")
            return False
        host = args[0] # IP of peer
        port = int(args[1]) # Port of peer
        print("Connecting to peer: {}:{}".format(host, port))
        try: # Try to connect and catch error on fail
            self.socket.connect((host, port))
        except socket.error:
            print("failedConnectingTimeout")
            return False
        # self.socket.send("\b/init {0} {1} {2}".format(self.chatApp.nickname, self.chatApp.hostname, self.chatApp.port).encode()) # Exchange initial information (nickname, ip, port)
        self.socket.sendto("You are connected to  {} {} {}".format(self.chatApp.nickname, self.chatApp.hostname, self.chatApp.port).encode(), (host, port))
        print("connected")
        self.isConnected = True # Set connection status to true
    
    # Method called by Chat App to reset client socket
    def stop(self):
        self.socket.close()
        self.socket = None

    # Method to send data to a peer
    def send(self, msg):
        if msg != '':
            try:
                self.socket.send(msg.encode())
                return True
            except socket.error as error:
                print("failedSentData")
                print(error)
                self.isConnected = False
                return False


    


