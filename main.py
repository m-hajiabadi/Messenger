import tkinter as tk
import socket
from myclient import Client
from myserver import Server
from datetime import datetime

class Messenger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peer to Peer Messenger")

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            self.hostname = s.getsockname()[0]
        except socket.error as error:
            self.hostname = "0.0.0.0"

        self.port = 0
        self.nickname = ""
        self.peer = ""
        self.peerIP = 0
        self.peerPort = 0

        self.res_pos = 0
        
        self.messageLog = []
        self.savedMessages = []

        self.rowconfigure([0, 1], minsize=400, weight=1)
        self.columnconfigure([0, 1], minsize=400, weight=1)

        self.frm_new_message = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frm_inputs = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frm_received_messages = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frm_history = tk.Frame(self, bg="yellow", relief=tk.RAISED, bd=2)

        self.lbl_received = tk.Label(self.frm_received_messages, text="")
        self.lbl_history = tk.Label(self.frm_history, text="", bg="yellow", anchor="n", justify=tk.LEFT)
        self.txt_message = tk.Text(self.frm_new_message)
        self.btn_send = tk.Button(self.frm_new_message, text="Send Message", command=self.send)

        self.lbl_name = tk.Label(self.frm_inputs, text="Name:")
        self.ent_name = tk.Entry(self.frm_inputs)

        self.lbl_port = tk.Label(self.frm_inputs, text="Port:")
        self.ent_port = tk.Entry(self.frm_inputs)

        self.btn_set_info = tk.Button(self.frm_inputs, text="Set my info", command=self.set_info)
        
        # self.lbl_peer_ip = tk.Label(self.frm_inputs, text="Peer IP:")
        # self.ent_peer_ip = tk.Entry(self.frm_inputs)

        self.lbl_peer_port = tk.Label(self.frm_inputs, text="Peer port:")
        self.ent_peer_port = tk.Entry(self.frm_inputs)

        self.btn_set_peer_info = tk.Button(self.frm_inputs, text="Set peer info", command=self.set_peer_info)
        
        self.btn_history = tk.Button(self.frm_history, text="Show History", command=self.show_history)

        self.frm_history.rowconfigure(0, minsize=380, weight=1)
        self.frm_history.columnconfigure(0, minsize=280, weight=1)

        self.lbl_received.grid(row=0, column=0, padx=5, pady=5)
        self.lbl_history.grid(row=0, column=0, padx=5, pady=5, sticky="ns")
        self.txt_message.grid(row=0, column=0)
        self.btn_send.grid(row=1, column=0, sticky="ew")

        self.lbl_name.grid(row=0, column=0, sticky=tk.W)
        self.ent_name.grid(row=0, column=1, sticky="ew")

        self.lbl_port.grid(row=1, column=0, sticky=tk.W)
        self.ent_port.grid(row=1, column=1, sticky="ew")
        self.btn_set_info.grid(row=2, column=0, sticky="ew")

        # self.lbl_peer_ip.grid(row=3, column=0, sticky=tk.W)
        # self.ent_peer_ip.grid(row=3, column=1, sticky="ew")

        self.lbl_peer_port.grid(row=4, column=0, sticky=tk.W)
        self.ent_peer_port.grid(row=4, column=1, sticky="ew")
        self.btn_set_peer_info.grid(row=5, column=0, sticky="ew")
        
        self.btn_history.grid(row=4, column=0, sticky="ew")

        self.frm_received_messages.grid(row=0, column=0, sticky="news")
        self.frm_inputs.grid(row=1, column=1, sticky="news")
        self.frm_history.grid(row=1, column=0, sticky="news")
        self.frm_new_message.grid(row=0, column=1, sticky="ew")
    
    def set_info(self):
        while self.nickname == "" or self.port == 0:
            self.nickname = self.ent_name.get()
            self.port = int(self.ent_port.get())
        
        # Start Server and Client threads
        self.chatServer = Server(self)
        self.chatServer.daemon = True
        self.chatServer.start()
        self.chatClient = Client(self)
        self.chatClient.start()
        
        self.ent_name.grid_forget()
        self.ent_port.grid_forget()
        
        self.lbl_name['text'] = self.nickname
        self.lbl_port['text'] = str(self.port)
        self.btn_set_info.grid_forget()
    
    def set_peer_info(self):
        if self.nickname and self.port:  
            # while self.peerIP == 0 or self.peerPort == 0:    
            #     self.peerIP = self.ent_peer_ip.get()
            #     self.peerPort = int(self.ent_peer_port.get())
            while self.peerPort == 0:    
                self.peerPort = int(self.ent_peer_port.get())
            self.peerIP = "127.0.0.1"
            # self.ent_peer_ip.grid_forget()
            self.ent_peer_port.grid_forget()
            
            # self.lbl_peer_ip['text'] = self.peerIP
            self.lbl_peer_port['text'] = str(self.peerPort)
            self.btn_set_peer_info.grid_forget()
            
            self.chatClient.conn([self.peerIP, self.peerPort])
            
        else:
            return
        
        
    
    def send(self):
        # while True:
        msg = self.txt_message.get("1.0", tk.END)
        while msg == "":
            msg = self.txt_message.get("1.0", tk.END)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {self.nickname} > {msg}"
        msg = f"{timestamp} - {msg}"

        # Append message to messageLog
        self.messageLog.append(log_message)

        # Save message to a file
        self.saveMessageLogToFile()

        if self.chatClient.isConnected:
            if self.chatClient.send(msg):
                print(f'{msg} Sent')
        else:
            print("notConnected")
        
        self.txt_message.delete("1.0", tk.END)
                 
    def loadMessagesFromFile(self):
        try:
            with open('saved_messages.txt', 'r') as file:
                lines = [line.strip() for line in file if line.strip()]
                return lines
        except FileNotFoundError:
            return []
        
    def saveMessageLogToFile(self):
        try:
            with open('saved_messages.txt', 'a') as file:
                for message in self.messageLog:
                    file.write(f"{message}\n")
            self.messageLog.clear()  # Clear the messageLog list after saving messages

        except Exception as e:
            print(f"Failed to save log: {e}")

    def show_history(self):
        self.savedMessages = self.loadMessagesFromFile()  # Load saved messages from file
        content = "\n".join(self.savedMessages)
        self.lbl_history.config(text=content)


if __name__ == "__main__":
    messenger = Messenger()
    messenger.mainloop()
