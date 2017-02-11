// SEST library. 2017, Alberto Chiusole


#include "SEST.h"
#include <Arduino.h>
#include "ESP8266WiFi.h"
// #include <string>

const char* ssid = "test";
const char* pswd = "test";
WiFiClient client;
const int httpPort = 80;

void setup() {
    Serial.begin(115200);
    delay(100);

    WiFi.begin(ssid, pswd);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }

    SEST sest(client);
}


void loop() {

}
