import socket
import threading

def broadcast(message, sender_socket):
    lock.acquire()
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())
    lock.release()

def handle_client(client_socket, address):
    while True:
        try:
            data_name = []
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                remove_client(client_socket)
                break

            else:
                broadcast(message, client_socket)

        except Exception as e:
            print(f"Error: {str(e)}")
            remove_client(client_socket)
            break

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 1234))
    server_socket.listen(5)
    print("Server listening on port 1234...")

    clients = []
    lock = threading.Lock()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Terhubung dengan {client_address}")
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()