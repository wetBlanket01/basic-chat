import socket
import random
from threading import Thread
from colorama import Fore, init
from datetime import datetime

init()

colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.YELLOW, Fore.BLACK
          ]

client_color = random.choice(colors)
colors.remove(client_color)

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
separator_token = '<SEP>'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"[*] Connecting to {SERVER_IP}:{SERVER_PORT}...")
client_socket.connect((SERVER_IP, SERVER_PORT))
print("[+] Connected.")

name = input('Enter your name: ')


def listen_for_message():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print('\n' + message + '\n> ', end='')
        except (ConnectionResetError, ConnectionAbortedError):
            print("\n[!] Server disconnected. Exiting...")
            client_socket.close()
            exit()


t = Thread(target=listen_for_message)
t.daemon = True
t.start()


while True:
    to_send = input('> ')

    if to_send.lower() == 'q':
        break

    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f'{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}\n'.encode()
    client_socket.send(to_send)

client_socket.close()
t.join()
