import sys
from ex2utils import Server

class MyServer(Server):
    def onStart(self):
        print("My server has started")
        self.active_clients = 0
        self.connections = []
        self.registered_users = {}  

    def onConnect(self, socket):
        print("A client has connected")
        self.active_clients += 1
        self.connections.append(socket)
        self.broadcast_active_clients()

    def onMessage(self, socket, message):
        parts = message.strip().split(' ', 1)
        if len(parts) >= 2:
            command = parts[0]
            parameters = parts[1]

            # Register
            if command.lower() == "register":
                if len(parameters.split()) == 1:
                    screen_name = parameters
                    if screen_name not in self.registered_users.values():
                        if socket not in self.registered_users:
                            self.registered_users[socket] = screen_name
                            socket.send(f"Successfully registered screen name: {screen_name}\n".encode())
                        else:
                            socket.send("You are already registered.\n".encode())
                    else:
                        socket.send(f"Screen name '{screen_name}' is already registered.\n".encode())
                else:
                    socket.send("Invalid command format. Please provide a single-word screen name.\n".encode())


            # Help 
            elif command.lower() == "help":
                help = "Invalid command. Please use 'help' without any parameter.\n"
                socket.send(help.encode())
                    


            # Message
            elif command.lower() == "message":
                if parameters.strip():
                    if socket in self.registered_users:
                        sender_name = self.registered_users[socket]
                        message_to_send = f"{sender_name}: {parameters}\n"
                        self.broadcast_message(message_to_send.encode())
                    else:
                        socket.send("You need to register a screen name before sending messages.\n".encode())
                else:
                    socket.send("Please try the message command again but with a message.\n".encode())

            # Direct Message
            elif command.lower() == "dm":
                if parameters.strip():
                    dm_parts = parameters.strip().split(' ', 1)
                    if len(dm_parts) == 2:
                        target_user = dm_parts[0]
                        dm_message = dm_parts[1]
                        if socket in self.registered_users:
                            sender_name = self.registered_users[socket]
                            if target_user in self.registered_users.values():
                                message_to_send = f"DM from {sender_name}: {dm_message}\n"
                                dm_sent = f"DM to {target_user}: {dm_message}\n"
                                self.send_dm(target_user, message_to_send.encode())
                                self.send_dm(sender_name, dm_sent.encode())
                            else:
                                socket.send(f"No user registered with the name '{target_user}'.\n".encode())
                        else:
                            socket.send("You need to register a screen name before sending direct messages.\n".encode())
                    else:
                        socket.send("Invalid command format. Please provide a user name or a message.\n".encode())
                else:
                    socket.send("Please try the dm command again but with a message.\n".encode())

            # List
            elif command.lower() == "list":
                if parameters.strip():
                    socket.send("Invalid command. Please use 'list' without any parameters.\n".encode())
                else:
                    user_list = [screen_name for screen_name in self.registered_users.values()]
                    if user_list:
                        user_list_str = ', '.join(user_list)
                        socket.send(f"Registered users: {user_list_str}\n".encode())
                    else:
                        socket.send("No registered users.\n".encode())
            else:
                socket.send("Invalid command. Type 'help' for a list of available commands.\n".encode())
        else:
            # Handling the case when no command is provided
            if not parts:
                error_message = "Please input a command.\n"
                socket.send(error_message.encode())
            else:
                # When only one part is provided, treat it as a message without a command
                message_content = parts[0]
                if message_content.lower() == "register":
                    socket.send("To register, please input a screen name.\n".encode())
                elif message_content.lower() == "list":
                    user_list = [screen_name for screen_name in self.registered_users.values()]
                    if user_list:
                        user_list_str = ', '.join(user_list)
                        socket.send(f"Registered users: {user_list_str}\n".encode())
                    else:
                        socket.send("No registered users.\n".encode())
                elif message_content.lower() == "help":
                    help_message = """
                    Available commands:
                    - register [screen_name]: Register a screen name.
                    - message [message]: Send a message to all registered users.
                    - dm [username] [message]: Send a direct message to a specific user.
                    - list: List all registered users.
                    - help: Display available commands and their usage.
                    """
                    socket.send(help_message.encode())
                else:
                    error_message = "Invalid command. Type 'help' for a list of available commands.\n"
                    socket.send(error_message.encode())

        return True

    def onDisconnect(self, socket):
        print("A client has disconnected")
        self.active_clients -= 1
        self.connections.remove(socket)
        if socket in self.registered_users:
            del self.registered_users[socket]  
        self.broadcast_active_clients()

    def broadcast_active_clients(self):
        message = f"Number of active clients: {self.active_clients}\n"
        message = message.encode()

        print(message.decode())

        for client_socket in self.connections:
            client_socket.send(message)

    def broadcast_message(self, message):
        for client_socket in self.connections:
            client_socket.send(message)

    def send_dm(self, target_user, message):
        for client_socket, screen_name in self.registered_users.items():
            if screen_name == target_user:
                client_socket.send(message)
                return
        print(f"User '{target_user}' not found for DM.")

ip = sys.argv[1]
port = int(sys.argv[2])

server = MyServer()

server.start(ip, port)
