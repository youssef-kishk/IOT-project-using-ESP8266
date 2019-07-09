
import threading
import socket
import sys, select, time


connections = []
publishersTopics = dict()                #topic_name:conn
subScriberTopics = dict()                #topic_name:[conn_list]
def createAcceptingSocket():
    try:
        global host
        global port
        global s
        host = "0.0.0.0"
        port = 8500
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
        connections.append((conn,address))
        thread = threading.Thread(target = handleClient, args = (conn,))
        thread.start()
    s.close()
    sys.exit()


def handleClient(conn):
    conn.settimeout(0)
    global publishersTopics
    global subScriberTopics
    clientPublishedTopics = []
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
                if 'Published topics:' in content.decode():
                    pTopicsIndex = str(content.decode()).find("Published topics")+17
                    publishedTopics = str(content.decode()[pTopicsIndex : str(content.decode()).find("/",pTopicsIndex)]).replace(" ","")
                    publishedTopics = publishedTopics.split(',')
                    for topic in publishedTopics:
                        publishersTopics[topic]=conn
                        clientPublishedTopics.append(topic)
                if 'Subscribed topics:' in content.decode():
                    sTopicsIndex = str(content.decode()).find("Subscribed topics:")+18
                    subscridedTopics = str(content.decode()[sTopicsIndex : str(content.decode()).find("/",sTopicsIndex)]).replace(" ","")
                    subscridedTopics = subscridedTopics.split(',')
                    for topic in subscridedTopics:
                        if topic in subScriberTopics:
                            subScriberTopics[topic].append(conn)
                        else:
                            connlist = [conn]
                            subScriberTopics[topic]= connlist
                if 'data' in content.decode():
                    start = True
                    continue
            else:
                content = conn.recv(streamDataSize)
                value = content.decode()
                if not("/" in content.decode()):
                    buffer.append(content.decode())
                else:
                    value = "".join(buffer)
                    buffer.clear()
                    if "end" in value:
                        break
                    # value = int(value)
                for topic in clientPublishedTopics:
                    if topic in subScriberTopics :
                        for connection in list(subScriberTopics[topic]):
                            connection.send(content)
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
                    # print(line)
            else:  # an empty line means stdin has been closed
                print('eof')
                exit(0)

    for topic in dict(publishersTopics):
        if publishersTopics[topic] == conn:
            del publishersTopics[topic]


    for topic in dict(subScriberTopics):
        for i in range(len(list(subScriberTopics[topic]))):
            if subScriberTopics[topic][i] == conn:
                del subScriberTopics[topic][i]
                break

    conn.close()

def terminal():
    global publishersTopics
    global subScriberTopics
    while True:
        command = input("")
        if command == "quit":
            print("exiting")
        if command == "topic list":
            topics = publishersTopics
            for topic in topics:
                print(topics)
        if command == "topic list sub":
            for topic in subScriberTopics:
                print(topic)
        if "echo topic " in command:
            print(command[11:])

def broker():
    global  subScriberTopics
    while True:
        for topic in dict(subScriberTopics):
            print("subScriberTopic",topic," ",subScriberTopics[topic])
        for topic in dict(publishersTopics):
            print("publishersTopic", topic, " ", publishersTopics[topic])

if __name__=="__main__":
    # thread = threading.Thread(target=terminal, args=())
    # thread.start()
    # thread = threading.Thread(target=broker, args=())
    # thread.start()
    createAcceptingSocket()
    startServer()
