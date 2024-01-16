import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.45.175', 9999))

    try:
        while True:
            message = input("Enter data (e.g., 'move 100 200'): ")
            client_socket.sendall(message.encode())

    except KeyboardInterrupt:
        pass

    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
