import threading
import socket
import wave, struct
import sys, select
import time

def createAcceptingSocket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 9000
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)
        bindSocket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bindSocket():
    try:
        global host
        global port
        global s
        global __maxNumberOfThreads__
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bindSocket()


# Establish connection with a client (socket must be listening)

def startServer():
    global __maxNumberOfThreads__
    while True:
        conn, address = s.accept()
        print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))
        thread = threading.Thread(target = handleClient, args = (conn,))
        thread.start()
        conn.send("yess".encode())
    s.close()
    sys.exit()


def handleClient(conn):
    sampleRate = 8000.0  # hertz
    obj = wave.open('sound.wav', 'w')
    obj.setnchannels(1)  # mono
    obj.setsampwidth(2)
    obj.setframerate(sampleRate)
    print("yess")
    conn.settimeout(0)
    streamDataSize = 1
    buffer = []
    start = False
    stop = False
    while True:
        if stop:
            break
        try:
            if not start:
                content = conn.recv(1024)
                if 'data' in content.decode():
                    start = True
                    continue
            else:
                content = conn.recv(streamDataSize)
                if not("/" in content.decode()):
                    buffer.append(content.decode())
                else:
                    value = "".join(buffer)
                    buffer.clear()
                    if "end" in value:
                        break
                    value = int(value)
                    data = struct.pack('<h', value)
                    obj.writeframesraw(data)
        except socket.error:
            pass
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()

            if line:
                if "exit" in line:
                    stop = True
                    conn.send("end/".encode())
                    break
                else:
                    conn.send(line.encode())
                    print(line)
            else:  # an empty line means stdin has been closed
                print('eof')
                exit(0)
    obj.close()
    print("closing")
    conn.close()

def run():

    createAcceptingSocket()
    startServer()



# run()