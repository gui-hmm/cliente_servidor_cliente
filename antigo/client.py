import socket
import threading

HEADER = 64
PORT = 5051
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "localhost"
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
            connected = False
        client.send(msg.encode(FORMAT))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
