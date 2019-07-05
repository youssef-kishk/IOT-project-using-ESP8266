import socket
import time
import afterUDPServer
import wave, struct

#################### Main Function ########################
sampleRate = 8000.0  # hertz
obj = wave.open('sound.wav', 'w')
obj.setnchannels(1)  # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
obj.close()
### Constants
PEER_ID = 1
UDP_SERVER_PORT = 9000
TCP_SERVER_PORT = 0     #fixed for all peers
UDP_BroadCast_PORT = 2000 #fixed for all peers


### UDP sender
Braodcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
Braodcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
Braodcaster.settimeout(0.2)
Braodcaster.bind(("", UDP_SERVER_PORT))
message = "Hello , it the client any body there"
# Braodcaster.sendto(message, ('<broadcast>', UDP_BroadCast_PORT))
Braodcaster.sendto(message.encode(), ('<broadcast>', UDP_BroadCast_PORT))
print("peer " + str(PEER_ID) + " message sent")
print("-----------------------------------------------------")
Braodcaster.close()
time.sleep(1)

### UDP client side
listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
listener.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
listener.bind(("", UDP_BroadCast_PORT))
#while True:
print("Entering Peer " + str(PEER_ID) + " listener-side")
data, addr = listener.recvfrom(50)
# peerID = data.decode().split("'")[1]
# print("received message from Peer" + peerID + ":%s" % data)
print("received message from Peer 2 :%s" % data , addr[0],addr[1])
print("-----------------------------------------------------")
listener.close()

Braodcaster = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
Braodcaster.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
Braodcaster.settimeout(0.2)
Braodcaster.bind(("", UDP_SERVER_PORT))
message = "let's start"
# Braodcaster.sendto(message, ('<broadcast>', UDP_BroadCast_PORT))
Braodcaster.sendto(message.encode(), (str(addr[0]), UDP_BroadCast_PORT))
print("peer " + str(PEER_ID) + " message sent")
print("-----------------------------------------------------")
Braodcaster.close()
time.sleep(1)



afterUDPServer.run()
