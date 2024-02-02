import socket

def receive_messages(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host} on port {port}")

        while True:
            # Receive data from the server
            data = s.recv(1024)  # Adjust buffer size as needed
            if not data:
                print("Connection closed by the server.")
                  # Exit if no data is received (server closed connection)
            print(f"Received from server: {data.decode('utf-8')}")

if __name__ == "__main__":
    HOST, PORT = '127.0.0.1', 12345
    receive_messages(HOST, PORT)
