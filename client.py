import socket
import sys

SERVER = '127.0.0.1'
PORT = 5001  # Port number

def connect_to_server():
    # Create a TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER, PORT))
        print(f"Connected to {SERVER} on port {PORT}")
        
        # Receive server's response
        response = client_socket.recv(1024)
        print("Server response:", response.decode())

if __name__ == "__main__":
    try:
        connect_to_server()
    except Exception as e:
        print(f"Failed to connect: {e}")

