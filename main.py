import tkinter as tk
from tkinter import messagebox
import socket
import threading
import datetime

class Messenger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Peer to Peer Messenger")
        self.geometry("800x800")

        self.messages = tk.Text(self, 
                                wrap=tk.WORD, 
                                bg="yellow",
                                bd=3,
                                cursor='arrow',
                                fg="blue",
                                tabs=30)
        self.messages.pack(pady=10)

        self.input_field = tk.Text(self, height=3, wrap='word')
        self.input_field.pack(pady=10)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

        self.messages.config(state=tk.DISABLED)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 8080))
        self.server.listen(1)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.conversation = []

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