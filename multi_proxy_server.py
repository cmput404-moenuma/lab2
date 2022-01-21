# for security
#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')

    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved. Exiting.")
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

def handle_proxy(addr, conn, host, port):

    # works like a client
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
        print("Connecting to Google")
        remote_ip = get_remote_ip(host)

        #connect proxy_end
        proxy_end.connect((remote_ip, port))

        #send data
        send_full_data = conn.recv(BUFFER_SIZE)
        print(f'Sending received data {send_full_data} to google')
        proxy_end.sendall(send_full_data)

        #remember to shut down (no more intention of read or write)
        proxy_end.shutdown(socket.SHUT_WR)

        data = proxy_end.recv(BUFFER_SIZE)
        print(f'Sending received data {data} to client')
        #send data back
        conn.send(data)

    conn.close() # deallocate memory


def main():
    host = 'www.google.com'
    port = 80

    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
    
        #QUESTION 3
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)

        print("Listening")
        
        #continuously listen for connections
        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            p = Process(target=handle_proxy, args=(addr, conn, host, port))
            p.daemon = True
            p.start()
            print("Started process", p)
            print("Connected by", addr)
            

if __name__ == "__main__":
    main()
