import socket
import threading
from encryption import ecb_decrypt, ecb_encrypt, cbc_decrypt, cbc_encrypt

clients = {}  # Dictionary to store clients with their IDs

def handle_client(conn, address, key, mode, iv=None):
    client_id = f"{address[0]}:{address[1]}"
    clients[client_id] = conn
    print(f"Connection from: {client_id}")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            # Decrypt the received message
            if mode.lower() == 'ecb':
                decrypt_msg = ecb_decrypt(data, key)
            elif mode.lower() == 'cbc' and iv is not None:
                decrypt_msg = cbc_decrypt(data, key, iv)
            else:
                print("Mode enkripsi tidak valid atau IV belum disediakan.")
                break

            print(f"from {client_id}: {decrypt_msg}")

            # Check if the message is directed to a specific client
            if decrypt_msg.startswith("@"):
                target_id, message = decrypt_msg[1:].split(" ", 1)
                if target_id in clients:
                    send_encrypted_message(clients[target_id], f"[{client_id} to you] {message}", key, mode, iv)
                else:
                    send_encrypted_message(conn, f"Client {target_id} tidak ditemukan.", key, mode, iv)
            else:
                broadcast_msg = f"[{client_id}] {decrypt_msg}"
                broadcast_message(conn, broadcast_msg, key, mode, iv)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()
        del clients[client_id]
        print(f"Connection closed: {client_id}")

def send_encrypted_message(client, message, key, mode, iv):
    if mode.lower() == 'ecb':
        encrypt_msg = ecb_encrypt(message, key)
    elif mode.lower() == 'cbc' and iv is not None:
        encrypt_msg = cbc_encrypt(message, key, iv)
    client.send(encrypt_msg.encode())

def broadcast_message(sender_conn, message, key, mode, iv):
    for client_id, client_conn in clients.items():
        if client_conn != sender_conn:
            send_encrypted_message(client_conn, message, key, mode, iv)

def server_program(key, mode, iv=None):
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    
    print("Server listening...")

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address, key, mode, iv))
        client_thread.start()

if __name__ == '__main__':
    key = input("Masukkan Key: ")
    mode = input("Pilih Mode Enkripsi (ecb/cbc): ")
    iv = None
    if mode.lower() == 'cbc':
        iv = input("Masukkan IV untuk CBC: ")
    server_program(key, mode, iv)
