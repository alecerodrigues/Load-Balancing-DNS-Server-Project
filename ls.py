import threading
import time
import random
import socket
import sys


dict = {}


def ls_listen_port():
    """
    This function is used to parse the ls port number argument from the console command.
    :return: int    -   The return is an integer that represents the port number to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[1]

    return int(arglist)


def ts1_hostname():
    """
    This function is used to parse the ts1 hostname argument from the console command.
    :return: str    -   The return is a string that represents the hostname to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[2]

    return arglist


def ts1_listen_port():
    """
    This function is used to parse the ts1 port number argument from the console command.
    :return: int    -   The return is an integer that represents the port number to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[3]

    return int(arglist)


def ts2_hostname():
    """
    This function is used to parse the ts2 hostname argument from the console command.
    :return: str    -   The return is a string that represents the hostname to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[4]

    return arglist


def ts2_listen_port():
    """
    This function is used to parse the ts3 port number argument from the console command.
    :return: int    -   The return is an integer that represents the port number to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[5]

    return int(arglist)


def client_connection():
    """
    This function starts the load server and performs the DNS lookups.
    :return: null
    """
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS -> C]: LS to Client socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', ls_listen_port())
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[LS -> C]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[LS -> C]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()

    print("[LS -> C]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    msg = "[LS -> C]: Connected to LServer"
    csockid.send(msg.encode('utf-8'))

    # receives dns query as a string
    dns_query = ''
    while dns_query != "done":
        dns_query = str(csockid.recv(1024)).rstrip()
        print(dns_query)


    # Close the server socket
    ss.close()


if __name__ == "__main__":

    time.sleep(random.random() * 5)
    ls_thread = threading.Thread(name='server', target=client_connection())
    ls_thread.start()