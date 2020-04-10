# Load-balancing-DNS-Server-Project
The aim of this project is to design and implement load balancing among
DNS servers by splitting the set of hostnames across multiple DNS servers.

_________________________________________

0. Authors

Alec Rodrigues (aer153)
Jared Montalbo (jvm104)

_________________________________________

1. Overview

The TS1 and TS2 server builds their DNS tables in a hash map provided by
their respective files (PROJ2-DNSTS1.txt) and (PROJ2-DNSTS2.txt). The client
first connects and sends the host names iteratively. LS proccesses these host names
by sending them to servers TS1 and TS2 and waits for a maximum of 5 seconds for a
response. If no response is recieved from TS1 and TS2 then LS sends an error message to
the client. If there is a response the LS sends the dns query to the client to be written
in resolved.txt.

_________________________________________

2. Known Problems

There are no known issues or functions in the attached code. The only way to cause an
issue is by not inputting values corrently.

_________________________________________

3. Issues in Development

Having to test 4 client/server scripts at once is an annoying process. Finding for
different devices to test it on and having to change arguments and keep track of
hostnames/port numbers was a troublesome process.

_________________________________________

4. What did we Learn?

We learned a lot about load balancing among DNS servers. Learning the design
in practice by splitting the set of hostnames across multiple DNS servers made
it more clear on how load balancing works. We also learned more technical
functions that can be used with sockets in python such as setting timeouts.