// SEST library.
// Alberto Chiusole -- 2017

#include "DHT.h"
#include "ESP8266WiFi.h"
#include "SEST.h"
#include <Arduino.h>
#include <string>

#include "secret_settings.h"

#define DHTTYPE DHT11 // I'm using the DHT 11
#define DHTPIN 4      // Wire DHT to GPIO4 on the ESP8266
DHT dht(DHTPIN, DHTTYPE);
enum field_meaning { TEMPERATURE, HUMIDITY };

const char* ssid = secret_ssid.c_str();
const char* pswd = secret_pswd.c_str();

const std::string channel = secret_channel;
const std::string key = secret_key;
WiFiClient client;
// const int httpPort = 80;
SEST sest(client, channel, key);

void setup() {
    Serial.begin(115200);
    delay(5000);

    Serial.print("SSID name: ");
    Serial.print(ssid);
    Serial.println();
    Serial.print("SSID password: ");
    Serial.print(pswd);
    Serial.println();

    WiFi.begin(ssid, pswd);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    dht.begin();
}

void loop() {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also take up to 2 seconds (its a very slow sensor).
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();
    // Read temperature as Fahrenheit (isFahrenheit = true)
    // float t_f = dht.readTemperature(true);

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t)) {
        // Serial.println("Failed to read from DHT sensor!");
        return;
    }

    Serial.println(String("Temperature: ") + t + "'C - Humidity: " + h + "%");

    sest.set_field(TEMPERATURE, t);
    sest.set_field(HUMIDITY, h);
    sest.push();

    // Wait 30 seconds before pushing again.
    delay(30000);
}
