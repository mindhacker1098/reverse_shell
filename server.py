import socket
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Server configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = int(os.getenv("PORT", 10000))  # Render's specified port or default to 10000
HTTP_PORT = 8000  # Use a different port for the HTTP server
BUFFER_SIZE = 1024 * 128

# Create a socket object
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# Bind the socket to the host and port
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(2)  # Listen for two connections (Admin and Worker)

print(f"Listening on {SERVER_HOST}:{SERVER_PORT} ...")

def run_http_server():
    class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("OK", "utf8"))
    
    server = HTTPServer(('0.0.0.0', HTTP_PORT), HealthCheckHandler)
    print(f"Starting HTTP server on port {HTTP_PORT}")
    server.serve_forever()

# Run the HTTP server in a separate thread
threading.Thread(target=run_http_server).start()

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
