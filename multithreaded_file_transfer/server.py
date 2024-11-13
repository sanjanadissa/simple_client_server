import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4466
ADDR=(IP,PORT)
SIZE = 1024
FORMAT ="utf-8"
SERVER_DATA_PATH = "server_data"

"""
CMD@Msg
"""

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")
    conn.send("OK@Welcome to the file server .".encode(FORMAT))
    
    while True:
        data = conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd =data[0]
        

        if cmd=="HELP":
            send_data = "OK@"
            send_data += " LIST : List all files in server \n"
            send_data += "  UPLOAD : Upload a file to server \n"
            send_data += "  DELETE : Delete a file from the server \n"
            send_data += "  LOGOUT : Disconnect from the server \n"
            send_data += "  HELP : List all commands"

            conn.send(send_data.encode(FORMAT))

        elif cmd == "LOGOUT":
            break

        elif cmd == "LIST":
            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directry is empty"
            else:
                send_data += "\n".join(f for f in files)
            conn.send(send_data.encode(FORMAT))

        elif cmd == "UPLOAD":
            name = data[1]
            text = data [2]

            filepath = os.path.join(SERVER_DATA_PATH,name)
            with open(filepath ,"w") as f:
                f.write(text)

            send_data = "OK@File uploaded"
            conn.send(send_data.encode(FORMAT))

        elif cmd == "DELETE":

            files = os.listdir(SERVER_DATA_PATH)
            send_data = "OK@"
            filename = data[1]

            print("Available files:", files)
            print("Requested filename to delete:", filename)

            if len(files) == 0:
                        send_data += "The server is empty"
            else:
                if filename in files:
                    file_path = os.path.join(SERVER_DATA_PATH, filename)
                    
                   
                    print("Constructed file path:", file_path)
                    
                    try:
                        os.remove(file_path)  
                        send_data += "File deleted"
                    except FileNotFoundError:
                        send_data += "File not found (FileNotFoundError)"
                    except Exception as e:
                        send_data += f"Error deleting file: {e}"
                        print("Exception occurred while deleting:", e)  
                else:
                    send_data += "File not found"

            conn.send(send_data.encode(FORMAT))
                 

    print(f"[DISCONNECTED] {addr} disconnected")

  
def main():
    print("[STARTING] server is starting")
    server =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("[listinng] server is listing")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

if __name__ =="__main__":
    main()
