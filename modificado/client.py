import socket
import threading

HEADER = 64
PORT = 5080
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"  # Use 'localhost' se estiver rodando na mesma máquina que o servidor
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    connected = True
    while connected:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                print(msg)
        except ValueError:
            print("[ERROR] Invalid message format")
        except ConnectionAbortedError:
            print("[ERROR] Server closed the connection")
            connected = False
        except ConnectionResetError:
            print("[ERROR] Server forcibly closed the connection")
            connected = False
    client.close()


def send():
    connected = True
    while connected:
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            client.send(msg.encode(FORMAT))
            connected = False
        else:
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
    client.close()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()

receive_thread.join()
send_thread.join()
