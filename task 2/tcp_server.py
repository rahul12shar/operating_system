import socket
import threading

HOST = '127.0.0.1'
PORT = 5555

clients = []
nicknames = []

def broadcast(message, sender_conn=None):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message)
            except:
                remove_client(client)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    conn.send("NICK".encode('utf-8'))
    nickname = conn.recv(1024).decode('utf-8')
    nicknames.append(nickname)
    clients.append(conn)
    
    print(f"[NICKNAME] {addr} is now known as {nickname}")
    broadcast(f"{nickname} joined the chat!".encode('utf-8'))
    conn.send("Connected to the server!".encode('utf-8'))
    
    connected = True
    while connected:
        try:
            message = conn.recv(1024)
            if message:
                formatted_msg = f"{nickname}: {message.decode('utf-8')}"
                print(f"[MESSAGE] {formatted_msg}")
                broadcast(formatted_msg.encode('utf-8'), conn)
            else:
                remove_client(conn)
                connected = False
        except:
            remove_client(conn)
            connected = False
    
    conn.close()

def remove_client(conn):
    if conn in clients:
        index = clients.index(conn)
        clients.remove(conn)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f"{nickname} left the chat!".encode('utf-8'))
        print(f"[DISCONNECT] {nickname} disconnected")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()