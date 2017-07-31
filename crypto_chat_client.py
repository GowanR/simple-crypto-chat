#####################################################################
#                                                                   #
#   `crypto_chat_client.py` is a client for encrypted messaging.    #
#   This software is for educational purposes.                      #
#                                                                   #
#   License: https://www.mozilla.org/en-US/MPL/                     #
#   Written by GowanR (Jul 30 2017)                                 #
#                                                                   #
#####################################################################


import socket
import threading
import sys
import os
import base64
from Crypto.Cipher import XOR
import base64
import getpass

help_text = """
--help -h           help menu (you're looking at it)

Usage:
python crypto_chat_client.py <sync port> <ip> <serer port>
python crypto_chat_client.py 8882 localhost 8881
"""

try:
    sys.argv[1]
    sys.argv[2]
    sys.argv[3]
except IndexError:
    print "Make sure you have the right arguments."
    print help_text
    exit(0)
os.system("clear")
intro_text = """
********************************************************
*                                                      *
*    Welcome to Chat Client Version 0.1.1              *
*                                                      *
*    Choose a username and just send messages!         *
*     (hint: don't use commas)                         *
*                                                      *
********************************************************
"""

print intro_text

def encrypt(key, plaintext):
  cipher = XOR.new(key)
  return cipher.encrypt(plaintext)

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  return cipher.decrypt(ciphertext)

sync_port = int(sys.argv[1])
server_ip = sys.argv[2]
server_port = int(sys.argv[3])
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = raw_input("Username: ")
passkey = getpass.getpass('Key: ')


def sync_messages():
    global passkey
    get_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_settings = ("localhost", int(sync_port))
    get_sock.bind(server_settings)
    get_sock.listen(2)
    while True:
        conn, addr = get_sock.accept()
        data = conn.recv(1024)
        data = data.split(",")
        if data[0] == "[Server]":
            print data[0] + ": " + data[1]
        else:
            print data[0] + ": " + decrypt(passkey, data[1])

sync_thread = threading.Thread(target=sync_messages)
sync_thread.start()
sock.connect((server_ip, server_port))
sock.send((str(username) + "," + str(sync_port)))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    while True:
        message = raw_input()
        sock.connect(("localhost", server_port))
        message = encrypt(passkey, message)
        sock.send((str(username) +"," + str(message)))
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except (KeyboardInterrupt, SystemExit):
    print("User ended.")
    sync_thread = None
