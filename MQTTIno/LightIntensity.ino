#include "WiFi.h"
#include "PubSubClient.h"
// Replace the next variables with your SSID/Password combination
const char* ssid = "";
const char* password = "";
// Add your MQTT Broker IP address, example:
const char* mqtt_server = "";
WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
// LED Pin
const int ledPin = 4;

const int photoResistorPin = 34;

void setup() {
  Serial.begin(115200);
  setup_wifi();
  
    client.setServer(mqtt_server, 1883);
  pinMode(ledPin, OUTPUT);
}
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messagein;
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messagein += (char)message[i];
  }
  if (topic == "room/light") {
    if (messagein == "ON")
      Serial.println("Light is ON");
  } else {
    Serial.println("Light is OFF");
  }
}
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("vanieriot")) {
      Serial.println("connected");
      client.subscribe("room/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  if (!client.loop())
    client.connect("vanieriot");
  int lightValue = analogRead(photoResistorPin);  
  Serial.print("Light Intensity: ");  
  Serial.println(lightValue);  

  char lightStr[10];
  snprintf(lightStr, sizeof(lightStr), "%d", lightValue);
  client.publish("IoT/light", lightStr);  

  delay(5000);
}
