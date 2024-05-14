import argparse
import socket
import threading
import sys

# clear line in terminal
def clear_line():
    print("\033[A\033[K", end="")


# function to rin client connection to server
def run(clientSocket, clientname):
    while True:
        try:
            # store msg
            message = clientSocket.recv(1024).decode()
            # send username to server
            if message == "getusername":
                clientSocket.send(clientname.encode())
            else:
                print(message)
        # close client connection if theres an error
        except:
            clientSocket.close()
            break


# function to send msgs to server
def sendMsg(clientSocket, clientname):
    while True:
        message = input()
        messagefull = f"{clientname}: {message}"
        clientSocket.send(messagefull.encode())
        # close client if exit is typed
        if message.lower() == "exit":
            print("Client Closing....")
            clientSocket.close()
            sys.exit(0)
        # clear console line
        clear_line()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argument Parser")
    parser.add_argument("name")  # to use: python tcp_client.py username
    args = parser.parse_args()
    client_name = args.name
    server_addr = "127.0.0.1"
    server_port = 9301

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    client_socket.connect((server_addr, server_port))

    run_thread = threading.Thread(target=run, args=(client_socket, client_name))
    run_thread.start()
    send_thread = threading.Thread(target=sendMsg, args=(client_socket, client_name))
    send_thread.start()

    # wait for the threads to finish before exiting
    run_thread.join()
    send_thread.join()

    # close the client socket
    client_socket.close()
