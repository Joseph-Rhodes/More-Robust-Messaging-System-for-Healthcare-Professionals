# COMP28112 Distributed Systems - Robust Messaging System

## Overview

This project is a **robust messaging system** for **healthcare professionals**, designed as part of the **COMP28112 Distributed Systems Coursework 2**. The project improves upon the first exercise by developing a **server-client message passing system** in Python.

## Features

- **Server:** Handles multiple client connections, processes commands, and maintains a registry of active users.
- **Client:** Sends messages to the server, registers a username, and supports direct messaging.
- **Command-Based Protocol:** Users can interact with the system using text-based commands.
- **GUI for Clients (Optional):** Provides a more user-friendly messaging experience.

## How to Run

### **Running the Server**

To start the server, open a terminal and run:

```sh
python3 myserver.py localhost 8090
```

The server will listen for client connections on **port 8090**.

### **Running the Client**

To start a client and connect to the server:

```sh
python3 myclient.py localhost 8090
```

This will open a pop-up window for the client to send and receive messages.

## Command List

The server supports the following commands:

1. `register <screen_name>` → Register a screen name.
2. `message <message>` → Send a message to all registered users.
3. `dm <screen_name> <message>` → Send a direct message to a specific user.
4. `list` → Display all registered users.
5. `help` → Show all available commands.

## 📄 View the Protocol Design Document

Click the link below to view the **Protocol Design Document** in a web browser:

[📖 View Protocol Design Document](./Protocol%20design%20document.pdf)

## Testing Instructions

### **Testing the Register Command**

- `register John` → Registers "John" if available.
- `register John Doe` → Error: Screen name must be **one word**.
- `register John` again → Error: "John" is already taken.

### **Testing Messaging**

- `message Hello everyone!` → Sends "Hello everyone!" to **all connected users**.
- `dm Alice Hey Alice!` → Sends a **private message** to Alice.

### **Testing Listing Users**

- `list` → Displays all **connected clients**.
- If no users are registered, returns `"No registered clients."`.

### **Testing Help Command**

- `help` → Displays the list of available commands.

