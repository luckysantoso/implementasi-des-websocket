import socket
import threading
from encryption import ecb_encrypt, ecb_decrypt, cbc_encrypt, cbc_decrypt

def receive_messages(client_socket, key, mode, iv=None):
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if data:
                if mode.lower() == 'ecb':
                    decrypt_msg = ecb_decrypt(data, key)
                elif mode.lower() == 'cbc' and iv is not None:
                    decrypt_msg = cbc_decrypt(data, key, iv)
                
                # Display the received message
                print('\n' + decrypt_msg)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

def client_program(key, mode, iv=None):
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    # Start a thread to listen for incoming messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, key, mode, iv))
    receive_thread.daemon = True
    receive_thread.start()

    # Send messages
    print("Ketik '@<ID> <pesan>' untuk mengirim pesan ke klien tertentu atau langsung kirim untuk broadcast.")
    message = input(" -> ")
    while message.lower().strip() != 'bye':
        if mode.lower() == 'ecb':
            encrypt_msg = ecb_encrypt(message, key)
        elif mode.lower() == 'cbc' and iv is not None:
            encrypt_msg = cbc_encrypt(message, key, iv)
        else:
            print("Mode enkripsi tidak valid atau IV belum disediakan.")
            break

        client_socket.send(encrypt_msg.encode())
        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    key = input("Masukkan Key: ")
    mode = input("Pilih Mode Enkripsi (ecb/cbc): ")
    iv = None
    if mode.lower() == 'cbc':
        iv = input("Masukkan IV untuk CBC: ")
    client_program(key, mode, iv)