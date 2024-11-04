import socket
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# Configuration
TCP_HOST = '0.0.0.0'  # Listen on all available interfaces for TCP
TCP_PORT = 5001       # Port to listen on for TCP connections
HTTP_PORT = 8000      # Port to listen on for HTTP health checks
LOG_FILE = 'connections.log'  # File to log TCP connections

def log_connection(client_address):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{datetime.now()} - Connection from {client_address}\n")
    print(f"Logged connection from {client_address}")


def start_tcp_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((TCP_HOST, TCP_PORT))
        server_socket.listen()
        print(f"TCP server listening on {TCP_HOST}:{TCP_PORT}")
        
        while True:
            # Accept a new connection
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected by {client_address}")
                log_connection(client_address)
                # Respond to client to confirm receipt
                client_socket.sendall(b"Connection logged.\n")


# Define HTTP Handler for health checks
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Respond with a 200 OK status for health checks
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK\n")

    def log_message(self, format, *args):
        return  # Suppress logging to avoid cluttering output


def start_http_server():
    http_server = HTTPServer(('0.0.0.0', HTTP_PORT), HealthCheckHandler)
    print(f"HTTP health check server listening on port {HTTP_PORT}")
    http_server.serve_forever()


if __name__ == "__main__":
    # Run the TCP server in a separate thread
    tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
    tcp_thread.start()
    
    # Run the HTTP server for health checks
    start_http_server()

