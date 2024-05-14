import os
import socket
import sys
import threading
import time 

#function for threading
def clielntConnection(connectionSocket):
    try:
        #request
        req = connectionSocket.recv(1024).decode()

        #fix file path
        filePath = req.split()[1]
        filePath = filePath[1:]
        
        #find file
        if os.path.isfile(filePath):
            with open(filePath, 'rb') as file:
                content = file.read()
        #create appropriate response
            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n'.encode() + content
            print('file found sendning msg...')
        else:
            response = 'HTTP/1.1 404 Not Found\r\n\r\nFile not found.'.encode()
            print('file not found')
    except:
        print('error')

    #close connection
    connectionSocket.sendall(response)
    connectionSocket.close()
    print('connection closed')


def main():

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #sys args
    port = int(sys.argv[1])
    maxClients = int(sys.argv[2])
    
    #start server
    serverSocket.bind((socket.gethostname(), port))
    print('server started on port:', port)

    #max connections
    serverSocket.listen(maxClients)

    #threading
    while True:
        try:
            connectionSocket, address = serverSocket.accept()
            clientThread = threading.Thread(target=clielntConnection, args=(connectionSocket,))
            clientThread.start()
        except:
            break
    
    #close server
    serverSocket.close()
    print('\nserver closed')
            
if __name__ == "__main__":
    main()
