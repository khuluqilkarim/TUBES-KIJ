import socket
import threading
import os
from datetime import datetime

def printc(text, color):
    print(f"\033[{color}m{text}\033[0m")

def benner():
    os.system('clear')

def clear():
    benner()

def gettime():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    return formatted_time

def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def send_text_message(client_socket, nama, message):
    time = gettime()
    encrypted_message = caesar_cipher(message, shift=3)
    formatted_message = f'{time} : {encrypted_message}'
    print(f"pesan yang di enkripsi : {encrypted_message}")
    client_socket.send(formatted_message.encode())

def receive_messages(client_socket):
    while True:
        try:
            encrypted_message = client_socket.recv(1024).decode()
            time_end = encrypted_message.find('m') + 1
            decrypted_message = caesar_cipher(encrypted_message[time_end:], shift=-3)
            print("Pesan di deskripsi : ",decrypted_message)
        except:
            printc("Terputus dari server", "31")
            client_socket.close()
            break

def start():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = "192.168.18.157"
    server_port = 1234
    nama = ""

    client_socket.connect((server_host, server_port))
    nama = input("Masukan Nama Anda :")
    print(f"\n{nama} Masuk kedalam Grup")

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    benner()

    while True:
        message = input('')
        if message.startswith("/clear"):
            clear()
        elif message.startswith("/quit"):
            client_socket.close()
            break
        else:
            send_text_message(client_socket, nama, message)

if __name__ == "__main__":
    start()
