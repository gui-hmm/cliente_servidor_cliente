import socket
import threading
HEADER = 64
PORT = 5060
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    """Envia mensagens para o servidor"""
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def receive():
    """Recebe mensagens do servidor"""
    while True:
        try:
            msg = client.recv(2048).decode(FORMAT)
            print(msg)
        except:
            print("An error occurred!")
            client.close()
            break

# Cria e inicia a thread para receber mensagens
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Loop para enviar mensagens
while True:
    msg = input()
    if msg == DISCONNECT_MESSAGE:
        send(DISCONNECT_MESSAGE)
        break
    send(msg)
send_thread = threading.Thread(target=send)
send_thread.start()
