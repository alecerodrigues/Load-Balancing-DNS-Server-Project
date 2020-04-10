import threading
import time
import random
import socket
import sys

dict = {}


def lookup(query):

    try:
        ip = dict[query.lower()]
        return query + ' ' + ip
    except:
        return 'none'


def populateTable():

    dnstablefile = open("PROJ2-DNSTS2.txt", "r")
    dnstable = dnstablefile.readlines()

    for i in dnstable:
        temp = i.split()

        dict[temp[0].lower()] = (temp[1] + ' ' + temp[2])
    return


def ts2_listen_port():
    """
    This function is used to parse the ts2 port number argument from the console command.
    :return: int    -   The return is an integer that represents the port number to bind to the port
    """
    fullargs = sys.argv
    arglist = fullargs[1]

    return int(arglist)


def ts1():

    # Initializes the LS -> Load Server connection
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS2]: TServer socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    populateTable()
    server_binding = ('', ts2_listen_port())
    ss.bind(server_binding)
    ss.listen(1)

    host = socket.gethostname()
    print("[TS2]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS2]: Server IP address is {}".format(localhost_ip))

    csockid, addr = ss.accept()

    print ("[TS2]: Got a connection request from a client at {}".format(addr))

    # send a intro message to the client.
    msg = "[TS2]: Connected to TServer 2"
    csockid.send(msg.encode('utf-8'))
    dns_query = str(csockid.recv(1024)).rstrip()
    while dns_query != 'EOD':
        # receives hostname to be queried
        time.sleep(random.random() * 5)
        # only send if nothing happens
        if lookup(dns_query) == 'none':
            csockid.send(dns_query + ' - Error:HOST NOT FOUND')
        else:
            csockid.send(lookup(dns_query))

        # should wait to recieve another query (at most 5 seconds)
        dns_query = str(csockid.recv(1024)).rstrip()

    # Close the server socket
    ss.close()


if __name__ == "__main__":
    time.sleep(random.random() * 5)
    t2 = threading.Thread(name='client', target=ts1())
    t2.start()

    time.sleep(5)
    print("Done. Output in RESOLVED.txt")