import socket
import os

# Server configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = int(os.getenv("PORT", 5003))  # Use Render's specified port or default to 5003
BUFFER_SIZE = 1024 * 128

# Create a socket object
s = socket.socket()

# Bind the socket to the host and port
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(2)  # Listen for two connections (Admin and Worker)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT} ...")

try:
    # Accept connection from the Worker
    print("Waiting for Worker connection...")
    worker_socket, worker_address = s.accept()
    print(f"Worker connected: {worker_address}")

    # Accept connection from the Admin
    print("Waiting for Admin connection...")
    admin_socket, admin_address = s.accept()
    print(f"Admin connected: {admin_address}")

    while True:
        try:
            # Receive command from admin
            command = admin_socket.recv(BUFFER_SIZE).decode()

            if command.strip().lower() == "exit":
                worker_socket.send(command.encode())  # Tell worker to exit
                break

            # Forward the command to the worker
            worker_socket.send(command.encode())

            # Receive the output from the worker
            worker_output = worker_socket.recv(BUFFER_SIZE).decode()

            # Forward the output back to the admin
            admin_socket.send(worker_output.encode())

        except (BrokenPipeError, ConnectionResetError):
            print("Connection with the worker has been lost.")
            break

finally:
    # Close the sockets when done
    worker_socket.close()
    admin_socket.close()
    s.close()
