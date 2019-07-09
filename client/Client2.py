#!/usr/bin/env python
import socket
import sys, select
import errno
import wave, struct



if __name__=="__main__":
    sampleRate = 3200.0  # hertz
    obj = wave.open('sound2.wav', 'w')
    obj.setnchannels(1)  # mono
    obj.setsampwidth(2)
    obj.setframerate(sampleRate)

    streamDataSize = 1
    buffer = []

    host = "3.17.184.50"
    port = 8000
    s = socket.socket()
    s.connect((host, int(port)))
    s.setblocking(0)
    s.send("http://1.1 GET/".encode())
    s.send("Published topics: node1 /".encode())
    s.send("Subscribed topics: voice1/".encode())
    s.send("data \n".encode())
    while True:
        try:
            data = s.recv(streamDataSize)
            if not ("/" in data.decode()):
                buffer.append(data.decode())
            else:
                value = "".join(buffer)
                buffer.clear()
                if "end" in value:
                    break
                value = int(value)
                data = struct.pack('<h', value)
                obj.writeframesraw(data)
        except IOError as e:  # and here it is handeled
            if e.errno == errno.EWOULDBLOCK:
                pass
        except struct.error:
            pass
        except ValueError:
            pass

        j, o, e = select.select([sys.stdin], [], [], 0.0001)
        if j == [sys.stdin]: break
    s.send("end/".encode())
    obj.close()
    s.close()
    print("yesss")