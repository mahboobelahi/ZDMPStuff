
import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_address = ('127.0.0.1', 5000)
print(f"Starting up on {server_address[0]} port {server_address}")
sock.bind(server_address)


sock.listen(1)


while True:
    print("Waiting for connection...")
    connection, client_address = sock.accept()

    print("Connection from ", client_address)

# import socket

# HOST = '192.168.100.2'  # Standard loopback interface address (localhost)
# PORT = 5000        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             if not data:
#                 break
#             conn.sendall(data)
