import tkinter as tk
from tkinter import messagebox
import socket
import threading
import datetime

class Messenger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peer to Peer Messenger")
        
        self.rowconfigure([0,1], minsize=400, weight=1)
        self.columnconfigure([0,1], minsize=400, weight=1)
        
        self.frm_new_message = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frm_received_messages = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frm_history = tk.Frame(self, bg="yellow", relief=tk.RAISED, bd=2)
        
        self.lbl_received = tk.Label(self.frm_received_messages, text="received_messages")
        self.lbl_history = tk.Label(self.frm_history, text="", bg="yellow")
        self.txt_message = tk.Text(self.frm_new_message)
        self.btn_send = tk.Button(self.frm_new_message, text="Send Message", command=None)
        self.btn_history = tk.Button(self.frm_history, text="Show History", command=None)
        
        self.frm_history.rowconfigure(0, minsize=380, weight=1)
        self.frm_history.columnconfigure(0, minsize=280, weight=1)
        
        self.lbl_received.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.lbl_history.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.txt_message.grid(row=0, column=0)
        self.btn_send.grid(row=1, column=0, sticky="ew")
        self.btn_history.grid(row=1, column=0, sticky="ew")                
        
        self.frm_received_messages.grid(row=0, column=0, sticky="news")
        self.frm_history.grid(row=1, column=0, sticky="news")
        self.frm_new_message.grid(row=0, column=1, sticky="ew")
        

        
        
        
        
    def send_message(self):
        message = self.input_field.get()
        if message:
            self.messages.config(state=tk.NORMAL)
            self.messages.insert(tk.END, f"You: {message}\n")
            self.messages.config(state=tk.DISABLED)
            self.input_field.delete(0, tk.END)

            # Add message to conversation history
            self.conversation.append((datetime.datetime.now(), "You", message))

            # Send message to other user
            client, address = self.server.accept()
            client.sendall(message.encode())

            # Save conversation history
            with open("conversation.txt", "w") as f:
                for timestamp, sender, msg in self.conversation:
                    f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {sender}: {msg}\n")

    def receive_messages(self):
        while True:
            client, address = self.server.accept()
            message = client.recv(1024).decode()

            # Add message to conversation history
            self.conversation.append((datetime.datetime.now(), "User", message))

            # Display message in GUI
            self.messages.config(state=tk.NORMAL)
            self.messages.insert(tk.END, f"User: {message}\n")
            self.messages.config(state=tk.DISABLED)

            # Save conversation history
            with open("conversation.txt", "w") as f:
                for timestamp, sender, msg in self.conversation:
                    f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {sender}: {msg}\n")

if __name__ == "__main__":
    messenger = Messenger()
    messenger.mainloop()