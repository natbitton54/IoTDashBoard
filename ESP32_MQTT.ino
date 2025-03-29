#include "WiFi.h"
#include "PubSubClient.h"

const char* ssid = "Sunskie"; // TP-Link_2AD8
const char* password = "4384060527"; // 14730078


const char* mqtt_server = "10.0.0.54";

WiFiClient espClient;
PubSubClient client(espClient);

const int lightPin = 34;
const int ledPin = 4;

void setup() {
  Serial.begin(115200);
  setup_wifi();
    client.setServer(mqtt_server, 1883);
  pinMode(ledPin, OUTPUT);
}

void setup_wifi() {
  delay(10);
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
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int lightVal = analogRead(lightPin);

  char message[10];
  sprintf(message, "%d", lightVal);
  client.publish("sensor/light", message);

  Serial.print("Light value: ");
  Serial.println(message);

  delay(5000);
}