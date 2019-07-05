# IOT-project-using-ESP8266
A simple IOT project in interfacing with ESP8266,

it consists of 2 parts:

First one is in case both the server and ESP client is connected to the same network so an UDP peer discovery is done first followed by a TCP connection is established then data streaming starts.

Second in case of different networks for both server and ESP client, the client keep pending waiting for a TCP handshaking to be made to start the connection and data streaming. 
