import socket
import threading
import time

class Server(threading.Thread): # Server object is type thread so that it can run simultaniously with the client
    def __init__(self, chatApp): # Initialize with a reference to the Chat App and initial vars
        super(Server, self).__init__()
        self.chatApp = chatApp
        self.port = self.chatApp.port # Get the server port from the Chat App reference
        self.host = "" # Accept all hostnames
        self.hasConnection = False # Connection status
        self.stopSocket = False # Socket interrupt status

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create new socket
        self.socket.bind((self.host, self.port)) # Bind the socket to host and port stored in the servers vars
        # self.socket.listen() # Set socket mode to listen



    # Method called by threading on start
    def run(self):
        
        while True: # Receive loop
            data, addr = self.socket.recvfrom(1024)  # Wait for data
            if not data: # If data is empty throw an error
                print("Received empty message")
                print("Disconnecting sockets")
                break

            print(data.decode())
            
            self.chatApp.lbl_received['text'] += data.decode() + "\n"


    def handleInit(self, init):
        if not init: # If initial information is empty, set peer vars to unknown
            self.chatApp.peer = "Unknown"
            self.chatApp.peerPort = "unknown"
            self.chatApp.peerIP = 'unknown'
        else: # Decode initial information and set peer vars to values send by peer
            init = init.decode()
            if init.startswith("\b/init"):
                init = init[2:].split(' ')
                self.chatApp.peer = init[1]
                self.chatApp.peerIP = init[2]
                self.chatApp.peerPort = init[3]
            else: # If initial information is not sent correctly 
                self.chatApp.peer = "Unknown"
                self.chatApp.peerPort = "unknown"
                self.chatApp.peerIP = 'unknown'

        if not self.chatApp.chatClient.isConnected: # Send message to inform about connectBack if client socket is not connected
            if self.chatApp.peerIP == "unknown" or self.chatApp.peerPort == "unknown":
                print("failedConnbackPeerUnknown")
            else:
                print("connbackInfo")
                print("connbackHostInfo")

        print("peerConnected")

    # Method called by Chat App to reset server socket
    def stop(self):
        if self.hasConnection:
            self.socket.close()
        else:
            self.stopSocket = True
            socket.socket(socket.AF_INET, socket.SOCK_DGRAM).connect(('localhost', self.port))
            time.sleep(0.2)
            self.socket.close()
        self.socket = None
        
        