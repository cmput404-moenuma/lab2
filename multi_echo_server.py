#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#echo connections back to client
def handle_echo(addr, conn):
    print("Connected by", addr)

    full_data = conn.recv(BUFFER_SIZE)
    conn.sendall(full_data)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    #create socket, bind, and set to listening mode
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #allow reused addresses
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)

        print("Listening")
        
        #continuously listen for connections
        while True:
            #accept connections and start a Proccess daeemon for handling multiple connections
            conn, addr = s.accept()
            p = Process(target=handle_echo, args=(addr, conn))
            p.daemon = True
            p.start()
            print("Started process", p)
            print("Connected by", addr)

if __name__ == "__main__":
    main()
