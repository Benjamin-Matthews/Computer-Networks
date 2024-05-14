import argparse
import socket
import sys
import threading
import random


#main method for running client server
def run(clientSocket, clientname, serverAddr, serverPort):
    #function to receive messages from the server
    def receiveMsg():
        while True:
            try:
                message, address = clientSocket.recvfrom(1024)
                message_text = message.decode()
                #split message to get sender and msg
                sender, msg = message_text.split(": ", 1)
                #check if sender is not the clientname and print msg
                if sender != clientname:
                    print(f"{sender}: {msg}")
            except:
                pass
    
    #thread for receiving messages from the server
    t = threading.Thread(target=receiveMsg)
    t.daemon = True
    t.start()

    #send message to server
    clientSocket.sendto(f"username:{clientname}".encode(), (serverAddr, serverPort))

    while True:
        #message input from the user
        message = input()
        #check if message is exit and close the connection
        if message == "exit":
            leave_message = f"leaving:{clientname}"
            clientSocket.sendto(leave_message.encode(), (serverAddr, serverPort))
            print("Client Closing....")
            t.join()
            clientSocket.close()
            sys.exit(0)
        else:
            #send message to the server if the message is not exit
            clientSocket.sendto(f"{clientname}: {message}".encode(), (serverAddr, serverPort))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')  
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    #udp socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.bind((serverAddr, random.randint(8000, 10000)))
    #run main fuction to start client server
    run(clientSocket, clientname, serverAddr, serverPort)
