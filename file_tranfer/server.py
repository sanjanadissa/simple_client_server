import socket

IP= socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (IP,PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    print("[STARTING] SErver is starting....")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[LISTING] server is listning")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        filename = conn.recv(SIZE).decode(FORMAT)
        print("[RECV] Filename received.")
        file = open( "serverdata/"+filename , "w")
        conn.send("Filename received.".encode(FORMAT))

        data = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] file data received.")
        file.write(data)
        conn.send("file data recived.".encode(FORMAT))


        file.close()
        conn.close()
        print(f"[DISCONNECTED] {addr} dissconnected")


if __name__ == "__main__":
    main()