import socket
import threading
import sys

intro_text = """
********************************************************
*                                                      *
*    Welcome to Chat Client Version 0.1.0              *
*                                                      *
*    Choose a username and just send messages!         *
*     (hint: don't use commas)                         *
*                                                      *
********************************************************
"""

print intro_text

server_port = sys.argv[1]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
username = raw_input("Username: ")

r_port = 8083

def sync_messages():
    get_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_settings = ("localhost", int(server_port))
    get_sock.bind(server_settings)
    get_sock.listen(2)
    while True:
	conn, addr = get_sock.accept()
	data = conn.recv(1024)
	data = data.split(",")
	print data[0] + ": " + data[1]
sync_thread = threading.Thread(target=sync_messages)
sync_thread.start()
sock.connect(("localhost", r_port))
sock.send((str(username) + "," + str(server_port)))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    while True:
        message = raw_input()
        sock.connect(("localhost", r_port))
        sock.send((str(username) +"," + str(message)))
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except (KeyboardInterrupt, SystemExit):
    print("User ended.")
    sync_thread = None
