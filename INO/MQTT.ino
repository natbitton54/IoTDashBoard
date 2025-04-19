#include <WiFi.h>
#include <PubSubClient.h>
#include <SPI.h>
#include <MFRC522.h>

const char* ssid = "Sunskie";
const char* password = "4384060527";
const char* mqtt_server = "10.0.0.54";

WiFiClient espClient;
PubSubClient client(espClient);

const int lightPin = 34;

#define SS_PIN 5
#define RST_PIN 4
MFRC522 rfid(SS_PIN, RST_PIN);

void setup_wifi() {
  delay(10);
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("esp32_combined")) {
      Serial.println("connected to MQTT");
      client.subscribe("room/light");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(lightPin, INPUT);

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

  int lightVal = analogRead(lightPin);
  char lightMessage[10];
  sprintf(lightMessage, "%d", lightVal);
  client.publish("sensor/light", lightMessage);
  Serial.print("Light value: ");
  Serial.println(lightVal);


  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
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

  delay(5000);
}
