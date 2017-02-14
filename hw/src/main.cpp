// SEST library.
// Alberto Chiusole -- 2017


#include "SEST.h"
#include <Arduino.h>
#include "ESP8266WiFi.h"

const char* ssid = "test";
const char* pswd = "test";
const char* address = "example.com/123/upload";
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

    SEST sest(client, address);
}


void loop() {

}
