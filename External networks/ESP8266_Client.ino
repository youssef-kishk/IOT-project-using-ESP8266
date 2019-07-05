
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#ifndef STASSID
#define STASSID "Phi Coworking Space"
#define STAPSK  "phi123456"
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

  const char* host = "3.14.246.29";
  const uint16_t port = 8000;
  //const char* host = "192.168.1.18";
 // const uint16_t port = 9000;

ESP8266WiFiMulti WiFiMulti;
WiFiClient client;
void setup() {
  Serial.begin(115200);

  // We start by connecting to a WiFi network
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP(ssid, password);

  Serial.println();
  Serial.println();
  Serial.print("Wait for WiFi... ");

  while (WiFiMulti.run() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("connecting to ");
  Serial.print(host);
  Serial.print(':');
  Serial.println(port);

  // Use WiFiClient class to create TCP connections

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    Serial.println("wait 5 sec...");
    return;
  }
  else{
      //read back one line from server
     client.print(String("GET /") + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n" +
                 "\r\n"
                );
    client.print("Published topics: voice1 /");
    client.print("Subscribed topics: node1 /");
    Serial.println("Sending data..");
   // String line = client.readStringUntil('\r');
   // Serial.println(line);
    client.print("/data");
    //delay(2000);
  }
}


void loop() {
  // This will send the request to the server
   client.print(random(-512,512));
   client.print("/");
  //Serial.println("closing connection");
  //client.stop();
  //Serial.end();
}

