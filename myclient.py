import tkinter as tk
from ex2utils import Client
import sys

class ChatGUI:
    def __init__(self, master, ip, port):
        self.master = master
        master.title("Simple Chat System")

        self.message_label = tk.Label(master, text="Welcome to the messaging system for healthcare professionals!", justify='left', anchor='w')
        self.message_label.pack(fill='both', expand=True)

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.send_button = tk.Button(master, text="Enter", command=self.send_message)
        self.send_button.pack()

        self.client = IRCClient(self)

        self.client.start(ip, port)

    def send_message(self):
        message = self.entry.get()
        self.client.send(message.encode())
        self.entry.delete(0, tk.END)

    def add_message(self, message):
        current_text = self.message_label['text']
        self.message_label.config(text=current_text + '\n' + message)

    def quit(self):
        self.client.stop()
        self.master.quit()

class IRCClient(Client):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui

    def onMessage(self, socket, message):
        self.gui.add_message(message)
        return True

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

root = tk.Tk()
app = ChatGUI(root, ip, port)
root.mainloop()
