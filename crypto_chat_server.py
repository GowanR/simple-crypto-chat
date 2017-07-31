import socket

intro_text = """
*****************************************************
*                                                   *
*   Chat Server Version 0.1.0                       *
*   Written by GowanR                               *
*                                                   *
*****************************************************
"""

print intro_text
messages = []
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8083))
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
            print "recv: ", data, "Address:", addr
        #for peer in addr_list:
        #    if peer != addr:
        #        push_sock.connect(peer)
        #        push_sock.send((data))
except (KeyboardInterrupt, SystemExit):
    print "\nShutting down server."
    sock.close()
