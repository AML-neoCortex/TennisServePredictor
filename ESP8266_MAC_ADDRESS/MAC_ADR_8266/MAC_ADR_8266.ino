#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(9600);
  delay(1000);
  
  // Print the MAC address of the ESP8266 module
  byte mac[6];
  WiFi.macAddress(mac);
  Serial.print("MAC address: ");
  for (int i = 0; i < 6; i++) {
    Serial.print(mac[i], HEX);
    if (i < 5) Serial.print(":");
  }
  Serial.println();
}

void loop() {
  // do nothing
}
