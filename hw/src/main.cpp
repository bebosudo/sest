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

const int TEMPERATURE = 1;
const int HUMIDITY = 2;

const char* ssid = secret_ssid.c_str();
const char* pswd = secret_pswd.c_str();

const std::string channel = secret_channel;
const std::string key = secret_key;
WiFiClient client;

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

    // Put the ESP8266 in station mode.
    WiFi.mode(WIFI_STA);
    // Disable the persistency (saving the WiFi network information to flash to
    // restore them at the next restart), since at each restart we explicitly
    // point the module to a specific network.
    WiFi.persistent(false);

    while (WiFi.status() != WL_CONNECTED) {
        WiFi.begin(ssid, pswd);
        delay(1000);
        Serial.print(".");
    }

    //dht.begin();

    // sest.set_port(8000);
}

void loop() {
    // TODO: check whether the ESP is still connected to the network at every
    // iteration.

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

    Serial.println(String("\n----------------\nTemperature: ") + t +
                   "'C - Humidity: " + h + "%\n");

    sest.set_field(TEMPERATURE, t);
    sest.set_field(HUMIDITY, h);

    std::string output;
    sest.push(output);
    Serial.print(output.c_str());
    Serial.println("**************\n");

    // Wait a while before pushing again.
    delay(6000);
}
