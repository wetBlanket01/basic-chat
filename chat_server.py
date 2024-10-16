import socket
from threading import Thread
import select

SERVER_IP = '0.0.0.0'
SERVER_PORT = 8080

separator_token = '<SEP>'

clients = set()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f'[*] Listening as {SERVER_IP}:{SERVER_PORT}')


def handle_client(client_socket):
    """
    Handles communication with a client.
    """
    while True:
        try:
            ready_to_read, _, _ = select.select([client_socket], [], [])

            if client_socket in ready_to_read:
                try:
                    message = client_socket.recv(1024).decode()

                    if message:
                        message = message.replace(separator_token, ': ').encode()
                        for client in clients:
                            if client != client_socket:
                                client.send(message)
                    else:
                        remove_client(client_socket)
                        break
                except ConnectionResetError:
                    remove_client(client_socket)
                    break

        except EOFError:
            remove_client(client_socket)


def remove_client(client_socket):
    """
    Removes a client from the list and closes the connection.
    """
    print(f"[!] {client_socket.getpeername()} disconnected.")
    clients.remove(client_socket)
    client_socket.close()


while True:
    try:

        ready_to_read, _, _ = select.select([server_socket] + list(clients), [], [])
        if server_socket in ready_to_read:
            client_socket, address = server_socket.accept()
            print(f'[+] {address} connected.')
            clients.add(client_socket)

            client_thread = Thread(target=handle_client, args=(client_socket,))
            client_thread.daemon = True

            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down...")
        break

for cs in clients:
    cs.close()

server_socket.close()
