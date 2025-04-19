#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char* ssid = "Sunskie";
const char* password = "4384060527";

const char* mqtt_server = "10.0.0.54";

#define SS_PIN 5
#define RST_PIN 4

MFRC522 rfid(SS_PIN, RST_PIN);
WiFiClient espClient;
PubSubClient client(espClient);

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

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" trying again in 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  SPI.begin(18, 19, 23, 5);
  rfid.PCD_Init();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
    return;
  }

  String rfidUID = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    rfidUID += (rfid.uid.uidByte[i] < 0x10 ? "0" : "");
    rfidUID += String(rfid.uid.uidByte[i], HEX);
  }
  rfidUID.toUpperCase();

  Serial.println("Card UID: " + rfidUID);

  client.publish("rfid/tag", rfidUID.c_str());

  delay(2000);
  rfid.PICC_HaltA();
}
