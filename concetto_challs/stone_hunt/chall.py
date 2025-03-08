import socket
import threading
import random
from secret import FLAG

PORT = 7250
max_piles = 1000  

def pile_gen():
    correct_weight = random.randint(1, 4)
    stones = [correct_weight] * max_piles

    fake_index = random.randint(0, max_piles - 1)

    fake_weight = random.randint(5, 10)
    stones[fake_index] = fake_weight

    return stones, fake_index + 1, fake_weight - correct_weight 

def handle_client(conn, addr):
    print(f"Connection from {addr}")
    
    stones, fake_index, weight_difference = pile_gen()
    print(f"{fake_index} and {weight_difference}")
    queries_left = 12

    welcome_message = b"""
     $$$$$$\    $$\                                         $$\   $$\                      $$\     
    $$  __$$\   $$ |                                        $$ |  $$ |                     $$ |    
    $$ /  \__|$$$$$$\    $$$$$$\  $$$$$$$\   $$$$$$\        $$ |  $$ |$$\   $$\ $$$$$$$\ $$$$$$\   
    \$$$$$$\  \_$$  _|  $$  __$$\ $$  __$$\ $$  __$$\       $$$$$$$$ |$$ |  $$ |$$  __$$\\_$$  _|  
     \____$$\   $$ |    $$ /  $$ |$$ |  $$ |$$$$$$$$ |      $$  __$$ |$$ |  $$ |$$ |  $$ | $$ |    
    $$\   $$ |  $$ |$$\ $$ |  $$ |$$ |  $$ |$$   ____|      $$ |  $$ |$$ |  $$ |$$ |  $$ | $$ |$$\ 
    \$$$$$$  |  \$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$$\       $$ |  $$ |\$$$$$$  |$$ |  $$ | \$$$$  |
     \______/    \____/  \______/ \__|  \__| \_______|      \__|  \__| \______/ \__|  \__|  \____/
        """

    conn.sendall(welcome_message)
    conn.sendall(b"\n\n =======================================================\n")
    conn.sendall(b"         Welcome to the Stone Hunt Challenge !\n")
    conn.sendall(b" =======================================================\n\n")
    conn.sendall(b"You have 1000 piles, each containing 1 stone. One pile has a fake stone with a different weight.\n")
    conn.sendall(b"Guess which pile the fake stone is in , and the difference between the fake and correct weight !\n")
    conn.sendall(b"You can make up to 12 queries to find the sum of weights of all stones in your specified range .\n")

    while queries_left > 0:
        conn.sendall(b"\nEnter two positions (l and r) separated by a space to query the sum on that range \n")
        conn.sendall(b"OR type 'guess' to guess the fake stone's index and weight difference : ")
        data = conn.recv(1024).decode().strip()

        if not data:
            break

        if data.lower() == "guess":
            conn.sendall(b"\nEnter your guess for the fake stone's index (1-1000): ")
            index_guess = conn.recv(1024).decode().strip()

            try:
                index_guess = int(index_guess)
                if index_guess < 1 or index_guess > 1000:
                    conn.sendall(b"Invalid input. Please enter a valid index between 1 and 1000.\n")
                    continue  
            except ValueError:
                conn.sendall(b"Invalid input. Please enter a valid integer.\n")
                continue  

            conn.sendall(b"Enter your guess for the weight difference between the fake and correct weight: ")
            weight_diff_guess = conn.recv(1024).decode().strip()

            try:
                weight_diff_guess = int(weight_diff_guess)
                if index_guess == fake_index and weight_diff_guess == weight_difference:
                    conn.sendall(f"Correct! Here's your flag: {FLAG} \n".encode())
                    break
                else:
                    conn.sendall(b"Wrong guess! Better luck next time.\n")
                    break
            except ValueError:
                conn.sendall(b"Invalid input. Please enter valid integers.\n")
                break


        try:
            l, r = map(int, data.split())
            if l >= r :
                conn.sendall(b"l must be strictly lesser than r !")
            elif 1 <= l < r <= max_piles:
                query_sum = sum(stones[l - 1:r])  
                conn.sendall(f"The sum of weights from position {l} to {r} is: {query_sum}\n".encode())
                queries_left -= 1
                conn.sendall(f"You have {queries_left} queries left.\n".encode())
            else:
                conn.sendall(b"Invalid input. Indices must be within the range 1 to 1000.\n")
        except ValueError:
            conn.sendall(b"Invalid input. Please follow the prompt format.\n")

    conn.sendall(b"Goodbye!\n")
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(5)
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
