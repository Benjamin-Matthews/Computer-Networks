import socket
import threading

clients = []  # list to add the connected client sockets


def run(serverSocket, serverPort):
    print("\nCHATROOM")
    print("This is the server side.\n")
    print(f"I am ready to receive connections on port {serverPort}")

    while True:
        # accept client connection
        clientSocket, clientAddress = serverSocket.accept()

        # add client to the clients list
        clients.append(clientSocket)

        # send username getter to the client
        clientSocket.send("getusername".encode())

        # get the username and store it
        username = clientSocket.recv(1024).decode()

        # print appropriate message of who joined with what username
        print(f"Message received from {clientAddress}: joining:{username}")
        print(
            f"User {username} has joined from address:{clientAddress[0]}:{clientAddress[1]}"
        )

        # threading for multiple connections
        clientThread = threading.Thread(target=clientConnection, args=(clientSocket,))
        clientThread.start()


# function to send msg to all users
def sendMsg(message):
    for client in clients:
        client.send(message)


# Handle client connection
def clientConnection(clientSocket):
    while True:
        try:
            # store msg from client
            message = clientSocket.recv(1024)
            if message:
                message_text = message.decode()

                parts = message_text.split(": ", 1)
                # strip msg to get content and username 
                if len(parts) == 2:
                    username = parts[0].strip()
                    message_content = parts[1].strip()
                clientAddress = clientSocket.getpeername()

                # close connection if exit is sent
                if message_content == "exit":
                    print(f"Message received from {clientAddress}: leaving:{username}")
                    break
                print(f"Message received from {clientAddress}: {username}:{message_content}" )
                sendMsg(message)
        except:
            break

    # Remove the client from the list
    clients.remove(clientSocket)

    # Close the client connection
    clientSocket.close()


if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM
    )  # Creating a TCP socket.
    server_socket.bind(("127.0.0.1", server_port))
    server_socket.listen(3)

    # keyboard interruput to close server
    try:
        run(server_socket, server_port)
    except KeyboardInterrupt:
        print("Server is shutting down...")
        # Close all client connections and the server socket
        for client in clients:
            client.close()
        server_socket.close()
