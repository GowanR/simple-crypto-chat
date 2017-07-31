##################################################################
#                                                                #
#   `crypto_chat_server.py` is a server for encrypted messaging. #
#   This software is written for educational purposes.           #
#                                                                #
#   License: https://www.mozilla.org/en-US/MPL/                  #
#   Written by GowanR (Jul 30 2017)                              #
#                                                                #
##################################################################
import socket
import sys

intro_text = """
*****************************************************
*                                                   *
*   Chat Server Version 0.1.1                       *
*   Written by GowanR                               *
*                                                   *
*****************************************************
"""
help_text = """
--help -h           help menu (you're looking at it)

Usage:
python crypto_chat_server.py <server ip> <port>
python crypto_chat_server.py localhost 8881
"""

try:
    sys.argv[1]
except IndexError:
    print "Please provide port argument"
    print help_text
    exit(0)

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print help_text
    exit(0)

local_ip = sys.argv[1]
port = int(sys.argv[2])

print intro_text
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((local_ip, port))
sock.listen(2)

user_list = []
port_list = []

def send_to_everyone(data):
    for i, user in enumerate(user_list):
        if not(user == data[0]):
            push_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            push_sock.connect(port_list[i])
            push_sock.send((str(data[0]) + "," + data[1]))
            push_sock.close()

try:
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        data = data.split(",")
        if not (data[0] in user_list):
            print "New user: ", data[0], str(addr[0]) + ":" + str(data[1])
            user_list.append(data[0])
            port_list.append((addr[0], int(data[1])))
            send_to_everyone(("[Server]", str(data[0]) + " connected."))
        else:
            send_to_everyone(data)
            #print "recv: ", data, "Address:", addr
except (KeyboardInterrupt, SystemExit):
    print "\nShutting down server."
    sock.close()
