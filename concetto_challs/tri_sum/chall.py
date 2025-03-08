import random
import threading
import socket
from secret import FLAG 

PORT = 7259

def num_gen():
    x = random.randint(1, 1000)
    y = random.randint(1, 1000)
    z = random.randint(1, 1000)
    return x, y, z

def reply(a, b, c, x, y, z):
    return (a * x) + (b * y) + (c * z)

def handle_client(client_socket):
    welcome_message = b'''
     $$$$$$$$\        $$\        $$$$$$\                          
     \__$$  __|       \__|      $$  __$$\                         
        $$ | $$$$$$\  $$\       $$ /  \__|$$\   $$\ $$$$$$\$$$$\  
        $$ |$$  __$$\ $$ |      \$$$$$$\  $$ |  $$ |$$  _$$  _$$\ 
        $$ |$$ |  \__|$$ |       \____$$\ $$ |  $$ |$$ / $$ / $$ |
        $$ |$$ |      $$ |      $$\   $$ |$$ |  $$ |$$ | $$ | $$ |
        $$ |$$ |      $$ |      \$$$$$$  |\$$$$$$  |$$ | $$ | $$ |
        \__|\__|      \__|       \______/  \______/ \__| \__| \__|
'''
    client_socket.send(welcome_message)
    client_socket.send(b"\n\nWelcome to the Number Guessing Challenge !\n\n")
    client_socket.send(b"Ethereum guessed three natural numbers : x , y , z\n\n")
    client_socket.send(b"You can ask him two queries using coefficients a , b , c separated by spaces to get ( a*x + b*y + c*z ) \n\n")
    client_socket.send(b"Your task is to find the values of x , y , z and return me the sum of squares of these numbers that is x^2 + y^2 + z^2 \n\n")
    client_socket.send(b"The values of x , y and z are sufficiently small ;) \n\n ")

    x, y, z = num_gen()

    client_socket.send(b"\nQuery 1: Enter the coefficients (a, b, c) : ")
    while True:
        try:
            coefficients = client_socket.recv(1024).decode().strip()
            a1, b1, c1 = map(int, coefficients.split())
            reply_1 = reply(a1, b1, c1, x, y, z)
            client_socket.send(f"Result of your first query: {reply_1}\n".encode())
            break  
        except ValueError:
            client_socket.send(b"Invalid input. Please enter three integers separated by spaces.\n")
        except Exception as e:
            client_socket.send(b"An error occurred. Please try again.\n")

    client_socket.send(b"\nQuery 2: Enter the coefficients (a, b, c) : ")
    while True:
        try:
            coefficients = client_socket.recv(1024).decode().strip()
            a2, b2, c2 = map(int, coefficients.split())
            reply_2 = reply(a2, b2, c2, x, y, z)
            client_socket.send(f"Result of your second query: {reply_2}\n".encode())
            break 
        except ValueError:
            client_socket.send(b"Invalid input. Please enter three integers separated by spaces.\n")
        except Exception as e:
            client_socket.send(b"An error occurred. Please try again.\n")

    answer = x**2 + y**2 + z**2
    client_socket.send(b"\nNow, guess the value of x^2 + y^2 + z^2:\n")

    while True:
        try:
            user_guess = client_socket.recv(1024).decode().strip()
            if user_guess == "":
                break 
            user_guess = int(user_guess)
            if user_guess == answer:
                client_socket.send(b"Congratulations! You've guessed correctly.\n")
                client_socket.send(f"Here's your flag: {FLAG}\n".encode())
                break
            else:
                client_socket.send(b"Sorry, that's incorrect. Goodbye !\n")
                break
        except ValueError:
            client_socket.send(b"Invalid input . Please enter an integer .\n")

    client_socket.close()
    print("connection closed")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", PORT))
    server.listen(40)
    print(f"server listening on port {PORT}...")

    while True:
        conn, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
