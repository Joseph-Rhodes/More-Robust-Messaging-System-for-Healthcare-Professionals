import sys
import threading
from ex2utils import Server

class MyServer(Server):
    def onStart(self):
        print("My server has started")
        self.active_clients = 0  
        self.connections = []  

    def onConnect(self, socket):
        print("A client has connected")
        self.active_clients += 1  
        self.connections.append(socket)  
        self.broadcast_active_clients()  

    def onMessage(self, socket, message):
        
        parts = message.strip().split(' ', 1)
        if len(parts) >= 2:
            command = parts[0]
            parameters = parts[1].split(' ')
            print("Command is ::", command)
            print("Parameters are ::", ', '.join(parameters))        
        else:
            print("Received message:", message)

        return True

    def onDisconnect(self, socket):
        print("A client has disconnected")
        self.active_clients -= 1  
        self.connections.remove(socket)  
        self.broadcast_active_clients()  

    def broadcast_active_clients(self):
        message = f"Number of active clients: {self.active_clients}\n"
        message = message.encode()

        print(message.decode())

        for client_socket in self.connections:
            client_socket.send(message)

ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

server.start(ip, port)
