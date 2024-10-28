import socket
from encryption import ecb_decrypt, ecb_encrypt, cbc_decrypt, cbc_encrypt

def server_program(key, mode, iv=None):
    host = socket.gethostname()
    port = 5000  

    server_socket = socket.socket()  
    server_socket.bind((host, port)) 
    
    server_socket.listen(2)
    conn, address = server_socket.accept()  
    print("Connection from: " + str(address))
    
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if mode.lower() == 'ecb':
            decrypt_msg = ecb_decrypt(data, key)
        elif mode.lower() == 'cbc' and iv is not None:
            decrypt_msg = cbc_decrypt(data, key, iv)
        else:
            print("Mode enkripsi tidak valid atau IV belum disediakan.")
            break

        print("from connected user: " + str(decrypt_msg))
        
        data = input(' -> ')
        
        if mode.lower() == 'ecb':
            encrypt_msg = ecb_encrypt(data, key)
        elif mode.lower() == 'cbc' and iv is not None:
            encrypt_msg = cbc_encrypt(data, key, iv)

        conn.send(encrypt_msg.encode()) 

    conn.close()  

if __name__ == '__main__':
    key = input("Masukkan Key: ")
    mode = input("Pilih Mode Enkripsi (ecb/cbc): ")
    iv = None
    if mode.lower() == 'cbc':
        iv = input("Masukkan IV untuk CBC: ")
    server_program(key, mode, iv)
