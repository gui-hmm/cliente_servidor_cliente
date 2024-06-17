import socket
import threading

HEADER = 64
PORT = 5080
SERVER = socket.gethostbyname(socket.gethostname())  # Obtém automaticamente o endereço IP local
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []  # Lista para armazenar todas as conexões dos clientes


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                    print(f"[{addr}] disconnected")
                else:
                    print(f"[{addr}] {msg}")
                    broadcast(msg)
        except ConnectionResetError:
            connected = False
            print(f"[{addr}] forcibly disconnected")
        except ValueError:
            connected = False
            print(f"[{addr}] invalid message format")

    conn.close()
    clients.remove(conn)


def broadcast(msg):
    for client in clients:
        client.send(msg.encode(FORMAT))


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")


print("[STARTING] server is starting...")
start()
