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

    #Setup TS1 Connection
    try:
        ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS -> TS1]: LS to TS1 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    temp_host = ts1_hostname()
    temp_port = ts1_listen_port()
    ts1_binding = (temp_host, temp_port)
    ts1.connect(ts1_binding)

    # Receive connect confirmation from TS1
    ts1_connect_conf = ts1.recv(100)
    print(ts1_connect_conf.decode('utf-8'))
    ts1.settimeout(5) # set timeout to 5 seconds of inactivity

    # Setup TS2 Connection
    try:
        ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS -> TS2]: LS to TS2 socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    temp_host2 = ts2_hostname()
    temp_port2 = ts2_listen_port()
    ts2_binding = (temp_host2, temp_port2)
    ts2.connect(ts2_binding)

    # Receive connect confirmation from TS1
    ts2_connect_conf = ts2.recv(100)
    print(ts1_connect_conf.decode('utf-8'))
    ts1.settimeout(5)  # set timeout to 5 seconds of inactivity

    # Process dns query recieved as a string
    dns_query = str(csockid.recv(1024)).rstrip()

    while dns_query != "EOD":
        #send queried hostname to ts1
        ts1.send(dns_query)
        ts2.send(dns_query)
        ts1_query_return = ''
        try:
            ts1_query_return = ts1.recv(100)
        except socket.timeout:
            print("[TS1 -> LS]: No Match Try TS2")
        #if don't recieve a response in 5 secs send back error


        ts2_query_return = ts2.recv(100)

        if ts1_query_return == (dns_query + ' - Error:HOST NOT FOUND'):
            csockid.send(ts2_query_return)
        #if ts2_query_return == (dns_query + ' - Error:HOST NOT FOUND'):
        else:
            csockid.send(ts1_query_return)
        dns_query = str(csockid.recv(1024)).rstrip()

    # Send EOD to TS1/TS2 (I don't think it hits in the loop)
    ts1.send(dns_query)
    ts2.send(dns_query)

    # Close the server socket
    ss.close()

if __name__ == "__main__":

    time.sleep(random.random() * 5)
    ls_thread = threading.Thread(name='server', target=client_connection())
    ls_thread.start()