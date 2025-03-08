import random
import socket
import threading
import time
from secret import FLAG

PORT = 7249
time_lim = 5 * 60  

def gen_arr():
    n = random.randint(11, 20)
    array = [random.randint(1, 100) for _ in range(n)]  
    return n, array

def session(conn, addr):
    print(f"Connection from {addr}")
    
    n, array = gen_arr()
    print(f"Generated array: {array}")  

    max_element = max(array)
    min_element = min(array)
    target_difference = max_element - min_element

    start_time = time.time()
    queries_left = n

    welcome_message = r"""
        $$$$$$$\  $$$$$$\ $$$$$$$$\ $$$$$$$$\ 
        $$  __$$\ \_$$  _|$$  _____|$$  _____|
        $$ |  $$ |  $$ |  $$ |      $$ |      
        $$ |  $$ |  $$ |  $$$$$\    $$$$$\    
        $$ |  $$ |  $$ |  $$  __|   $$  __|   
        $$ |  $$ |  $$ |  $$ |      $$ |      
        $$$$$$$  |$$$$$$\ $$ |      $$ |      
        \_______/ \______|\__|      \__|      
    """


    conn.sendall(welcome_message.encode())
    conn.sendall(b"==========================================\n")
    conn.sendall(b"       Welcome to the Difference Challenge!   \n")
    conn.sendall(b"    ==========================================\n")
    conn.sendall(f"The challenge consists of {n} hidden elements.\n".encode())
    conn.sendall(f"You can make up to {n} queries to find the sum of elements at two positions.\n".encode())
    conn.sendall(b"You need to guess the difference between the largest and smallest elements.\n")
    conn.sendall(b"\nHere's an example to help you out:\n")
    conn.sendall(b"Suppose you enter 1 2 , we'll give you the sum of the numbers in positions 1 and 2 from the list.\n")

    while queries_left >= 0:
        if time.time() - start_time > time_lim:
            conn.sendall(b"Time's up! Please reconnect to try again.\n")
            break

        conn.sendall(b"\nEnter two positions separated by a space to find their sum")
        conn.sendall(b"\nOR type 'guess' to guess the difference: ")
        data = conn.recv(1024).decode().strip()

        if not data:
            break

        if data.lower() == "guess":
            conn.sendall(b"\nEnter your guess for the difference between the largest and smallest numbers: ")
            guess = conn.recv(1024).decode().strip()

            try:
                guess = int(guess)
                if guess == target_difference:
                    conn.sendall(f"\nCorrect! Here's your flag: {FLAG}\n".encode())
                else:
                    conn.sendall(b"\nWrong guess! Better luck next time.\n")
            except ValueError:
                conn.sendall(b"Invalid input. Please enter a valid integer.\n")
            break

        try:
            i, j = map(int, data.split())

            if 0 < i <= n and 0 < j <= n:
                if i == j:
                    conn.sendall(b"Haha you thought it would be that easy?\n")
                else:
                    query_sum = array[i-1] + array[j-1]
                    conn.sendall(f"The sum of numbers at positions {i} and {j} is: {query_sum}\n".encode())
                    queries_left -= 1
                    conn.sendall(f"You have {queries_left} queries left.\n".encode())
            else:
                conn.sendall(b"Invalid input. Indices must be within the range\n")
        except ValueError:
            conn.sendall(b"Invalid input. Mind reading the prompt properly ?\n")

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

