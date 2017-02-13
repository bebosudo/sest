// SEST library.
// Alberto Chiusole -- 2017


#include "SEST.h"
#include <Arduino.h>
#include "ESP8266WiFi.h"

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

    uint32_t ch_id = 12;
    SEST sest(client, ch_id);
}


void loop() {

}
