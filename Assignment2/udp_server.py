# Libraries and Imports
import socket
import threading
import queue
import sys 

#queue to store the messages
message_queue = queue.Queue()
#dict to store the connected clients
clients = {}
#welcome message
print("\nCHATROOM")
print("This is the server side.\n")
print(f"I am ready to receive connections on port {9301}")

#function for receiving messages from clients
def receiveMsg():
    while True:
        #add msg to the queue
        try:
            message, address = serverSocket.recvfrom(1024)
            message_queue.put((message, address))
        except:
            break  

#function for sending messages to clients
def sendMsg():
    while True:
        #check if there are any messages in the queue to send
        while not message_queue.empty():
            message, address = message_queue.get()
            #decode the message  
            message_text = message.decode()  
            #check if address is not in the clients dict to add a new client
            if address not in clients:
                clients[address] = None
                #add username to the clients dict
                if message_text.startswith("username"):
                    username = message_text[message_text.index(":") + 1:]
                    clients[address] = username
                    #print appropriate message of who joined with what username
                    print(f"Message received from {address}: joining:{username}")
                    print(f"User {username} has joined from address: {address[0]}:{address[1]}")
            else:
                #print appropriate message when username is already in the clients dict and client sent a msg
                print(f"Message received from {address}: {message_text}" )
                #send the msg to all connected clients
                for client_address, username in clients.items():
                    if address != client_address:
                        serverSocket.sendto(message, client_address)

def run(serverSocket, serverPort):
    #threads for multiple connections
    t1 = threading.Thread(target=receiveMsg)
    t2 = threading.Thread(target=sendMsg)

    t1.start()
    t2.start()

    #wait for the threads to finish to shut down server
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print("Server shutting down...")
        serverSocket.close()  #close the server socket
        sys.exit(0)  #exit the program
        

if __name__ == "__main__":
    serverPort = 9301 
    #udp socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    serverAddr = '127.0.0.1'
    serverSocket.bind((serverAddr, serverPort))
    #calling the function to start the server
    run(serverSocket, serverPort)  
