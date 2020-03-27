import threading
import time
import random
import socket
import sys
import os


def ls_hostname():
    """
    This function is used to parse the ls hostname argument from the console command.
    :return: str    -   The return is a string that represents the hostname to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[1]

    return arglist


def ls_listen_port():
    """
    This function is used to parse the ls port number argument from the console command.
    :return: int    -   The return is an integer that represents the port number to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[2]

    return int(arglist)


def client():

    # Initializes the Client -> Load Server connection
    try:
        ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # Binds the ls port and creates the connection
    ls_port = ls_listen_port()
    ls_name = ls_hostname()  # localhost for self
    ls_binding = (ls_name, ls_port)
    ls.connect(ls_binding)

    # Receive connect confirmation from LS
    ls_connect_conf = ls.recv(100)
    print(ls_connect_conf.decode('utf-8'))

    # Generates the resolved hostname list
    if os.path.exists("RESOLVED.txt"):
        os.remove("RESOLVED.txt")
    resolved_queries = open("RESOLVED.txt", "a")

    # Generates the query list from the text file
    query_list_file = open("PROJ2-HNS.txt", "r")
    query_list = query_list_file.readlines()

    for query in query_list:

        # Send Hostname being queried to RS
        hostname = query
        ls.sendall(hostname.encode())

    end_flag = "done"
    ls.sendall(end_flag.encode())
    ls.close()
    exit()


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=client)
    t2.start()

    time.sleep(5)
    print("Done. Output in RESOLVED.txt")