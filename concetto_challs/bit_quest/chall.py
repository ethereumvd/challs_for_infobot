import random
import socket
import threading
import time
from secret import FLAG

#time_limit = 15  
max_tries = 20
str_len = 10
PORT = 8096

def gen_string(n):
    return ''.join(random.choice('01') for _ in range(n))

def session(conn, addr):
    print(f"Connection from {addr}")
    
    target = gen_string(str_len)
    print(f"Generated binary string: {target}")
    
    tries = 0
    #   start_time = time.time()

    welcome_message = r"""

    $$$$$$$\  $$$$$$\ $$$$$$$$\        $$$$$$\  $$\   $$\ $$$$$$$$\  $$$$$$\ $$$$$$$$\ 
    $$  __$$\ \_$$  _|\__$$  __|      $$  __$$\ $$ |  $$ |$$  _____|$$  __$$\\__$$  __|
    $$ |  $$ |  $$ |     $$ |         $$ /  $$ |$$ |  $$ |$$ |      $$ /  \__|  $$ |   
    $$$$$$$\ |  $$ |     $$ |         $$ |  $$ |$$ |  $$ |$$$$$\    \$$$$$$\    $$ |   
    $$  __$$\   $$ |     $$ |         $$ |  $$ |$$ |  $$ |$$  __|    \____$$\   $$ |   
    $$ |  $$ |  $$ |     $$ |         $$ $$\$$ |$$ |  $$ |$$ |      $$\   $$ |  $$ |   
    $$$$$$$  |$$$$$$\    $$ |         \$$$$$$ / \$$$$$$  |$$$$$$$$\ \$$$$$$  |  $$ |   
    \_______/ \______|   \__|          \___$$$\  \______/ \________| \______/   \__|
                                       \___|
    """

    conn.sendall(welcome_message.encode())
    conn.sendall(b"  < ----------------- Welcome to the Binary Guessing Game! ----------------- >\n")
    conn.sendall(b"      < ------------- Try to guess the 10-character binary string -------------- >\n")
    conn.sendall(b"      < -------------------- You can make up to 20 queries --------------------- >\n")

    while tries <= max_tries:
#        if time.time() - start_time > time_limit:
#          conn.sendall(b"Time's up! Please reconnect.\n")
#           break

        conn.sendall(b"\nEnter a binary string to query or enter 'guess' to guess the whole string: ")
        data = conn.recv(1024).decode().strip()

        if not data:
            break

        if data.lower() == "guess":
            conn.sendall(b"Enter your guess for the full binary string: ")
            guess = conn.recv(1024).decode().strip()
            
            if guess == target:
                conn.sendall(f"Correct! Here's your flag: {FLAG}\n".encode())
            else:
                conn.sendall(b"Wrong guess! Better luck next time.\n")
            break

        if len(data) > str_len or not all(c in '01' for c in data):
            conn.sendall(b"Invalid input. Please enter a valid binary string.\n")
            continue

        if data in target:
            conn.sendall(b"Yes, it's a substring!\n")
        else:
            conn.sendall(b"No, it's not a substring.\n")

        tries += 1
        conn.sendall(f"You have {max_tries - tries} queries left.\n".encode())

    conn.sendall(b"Goodbye!\n")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=session, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()

