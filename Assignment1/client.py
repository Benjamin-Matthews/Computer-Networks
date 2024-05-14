import socket
import sys

#sys args
port = int(sys.argv[1])
fileName = sys.argv[2]

#connect to server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((socket.gethostname(), port))
print('connection established\n')

#send request
req = f'GET /{fileName} HTTP/1.1\r\nHost: localhost\r\n\r\n'
clientSocket.send(req.encode())

response = clientSocket.recv(1024)

print('msg received\n')

responseStr = ""
#create response string and save file
with open(f'downloaded: {fileName}', 'wb') as file:
    #remove headers
    response = response.split(b'\r\n\r\n', 1)[1] 
    while response:
        file.write(response)
        responseStr += response.decode()
        response = clientSocket.recv(1024)

print(responseStr)

#close connection
clientSocket.close()
print('\nconnection closed')
