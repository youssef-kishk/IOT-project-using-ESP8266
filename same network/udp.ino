#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <ESP8266WiFiMulti.h>


//const char *ssid = "Ink Coworking space";
//const char *pass = "44332211";

//const char *ssid = "youssef";
//const char *pass = "1234567890";

const char *ssid = "Phi Coworking Space";
const char *pass = "phi123456";

unsigned int localport = 2000;


ESP8266WiFiMulti WiFiMulti;
WiFiClient client;

IPAddress sendIp (192,168,43,255);
WiFiUDP udp;

char recieveBuffer [50];
String string;
char sendBuffer[50];

int recievePacket(){
  int packetSize = udp.parsePacket();
  if(packetSize){
    int len = udp.read(recieveBuffer,255);
    if(len>0){
      recieveBuffer[len]=0;
    }
    Serial.println(recieveBuffer);
  }
}
void setup(){
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, pass);

  
  Serial.println();
  WiFi.begin(ssid,pass);

  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.print("..");
  }

  Serial.print("\nESP8266-> Connected to ");
  Serial.println(ssid);
  Serial.print("ESP8266-> IP: ");
  Serial.println(WiFi.localIP());
  
  Serial.println("ESP8266-> UDP is starting");
  udp.begin(localport);
  Serial.print("ESP8266-> Port: ");
  Serial.println(udp.localPort());

  Serial.println("ESP8266-> Broadcast Listening, waiting");
  
  //wait for udp connection
  int packetSize = udp.parsePacket();
  while(packetSize==0){packetSize = udp.parsePacket();Serial.print(".");delay(500);}
  if(packetSize){
    int len = udp.read(recieveBuffer,255);
    if(len>0){
      recieveBuffer[len]=0;
    }
    Serial.print("\nRecieved-> ");
    Serial.println(recieveBuffer);
  }

   
   char buffers[1000];
   String s = "UDP Connection done, Hello form ESP8266!";
   packetSize=0;
   while(packetSize==0){
       s.toCharArray(buffers,1000);
       udp.beginPacket(sendIp,localport);
       udp.write(buffers);
       udp.endPacket();
       packetSize = udp.parsePacket();
   }
   int len = udp.read(recieveBuffer,255);
   if(len>0){
         recieveBuffer[len]=0;
     }
     Serial.print("Recieved-> ");
    Serial.println(recieveBuffer);


  //TCP
  delay(1000);
  IPAddress connectedIP = udp.remoteIP();
  unsigned int connectedPort = udp.remotePort();
  Serial.print("ESP8266-> connecting to ");
  Serial.print(connectedIP);
  Serial.print(':');
  Serial.println(connectedPort);

    // Use WiFiClient class to create TCP connections
  if (!client.connect(connectedIP, connectedPort)) {
    Serial.println("connection failed");
    return;
  }
  else{
      //read back one line from server
     client.print(String("GET /") + " HTTP/1.1\r\n" +
                 "Host: " + connectedPort + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );
     Serial.println("TCP connection Done");
     client.print("data/");
     delay(1000);
  }
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH); 
}

void loop(){

  //check end/
  String line = "";
  client.setTimeout(1);
  Serial.println("Sending data Streaming");
  while(line!="end"){
    client.print(random(-512,512));
    client.print("/");
    line = client.readStringUntil('/');
    if(line.equals("on")){
      digitalWrite(LED_BUILTIN,LOW);    
    }
   else if(line.equals("off")){
    digitalWrite(LED_BUILTIN,HIGH); 
   }
    
  }
  Serial.print("reseted");
  delay(1000);
  ESP.restart(); 
  
}

