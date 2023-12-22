import socket
import threading

def handle_client_file(client_socket):
    filename = client_socket.recv(1024).decode("utf-8")
    file_data = client_socket.recv(1024)

    # Ambil ekstensi file dari nama file
    ext = filename.split(".")[-1]
    print(filename)

    # Cek apakah ekstensi file termasuk yang diizinkan
    allowed_extensions = [".txt", ".png", ".pdf", ".js"]
    if ext in allowed_extensions:
        # Panggil fungsi untuk mengurus pengiriman file
        save_path = f"{filename}"  # Ganti dengan direktori tempat menyimpan file
        save_file(file_data, save_path)
    else:
        # Ekstensi file tidak diizinkan, berikan pesan ke client
        client_socket.send("File extension not allowed.".encode())

def save_file(file_data, save_path):
    with open(save_path, "wb") as file:
        file.write(file_data)
    print(f"File berhasil disimpan: {save_path}")

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
                # Client disconnects
                remove_client(client_socket)
                break

            if str(message).startswith("/file"):
                data_name.append(address)
                handle_client_file(client_socket,address)

            else:
                # Jika bukan file, broadcast pesan ke seluruh client
                broadcast(message, client_socket)

        except Exception as e:
            # Terjadi error, client disconnects
            print(f"Error: {str(e)}")
            remove_client(client_socket)
            break

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

if __name__ == '__main__':
    # Inisialisasi server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)
    print("Server listening on port 12345...")

    # List untuk menyimpan koneksi client
    clients = []
    lock = threading.Lock()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Terhubung dengan {client_address}")
        clients.append(client_socket)

        # Jalankan thread untuk menghandle client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()