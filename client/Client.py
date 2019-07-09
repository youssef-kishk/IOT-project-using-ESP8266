import socket
import sys, select
import errno

from random import randint
if __name__=="__main__":

    host = "0.0.0.0"
    port = 9000
    s = socket.socket()
    s.connect((host, int(port)))
    s.setblocking(0)
    s.send("http://1.1 GET/".encode())
    s.send("Client name: Streamer /".encode())
    s.send("Published topics: voice1/".encode())
    s.send("Subscribed topics: node1/".encode())
    s.send("data \n".encode())
    while True:
        try:
            data = s.recv(1024)
            if "end/" in data.decode():
                break
        except IOError as e:  # and here it is handeled
            if e.errno == errno.EWOULDBLOCK:
                pass
        try:
            number = randint(-512,512)
            value = (str(number)+"/").encode()
            s.send(value)
            # print(value)
        except ValueError:
            pass
        j, o, e = select.select([sys.stdin], [], [], 0.0001)
        if j == [sys.stdin]: break
    s.send("end/".encode())
    s.close()
    print("yesss")