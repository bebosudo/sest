# Setup

## Wiring

UART usb converter:
* ground: brown;
* rx: red;
* tx: orange;
* power5v: yellow;
* reset: green.

to the ESP8266:
* brown: blue GND;
* red: brown, RX, to the zener diode configuration (with the resistance and the zener diode for the voltage partitor);
* orange: green, TX;
* yellow: orange, 5V;
* green: orange with red stripes, REST.

(place the ESP8266 with TX on 15th hole of the breadboard).

Follow the report [AlbertoChiusole-Elettronica_adattatoreArduino-ESP8266.pdf](./AlbertoChiusole-Elettronica_adattatoreArduino-ESP8266.pdf) for the AMS1117 and the Zener diode config.

Place a resistance of 1-10 kOhm between GND and GPIO15, and a similar one between CH_PD ('EN' in the scheme below) and VCC (3.3V).

Leftmost foot of AMS1117 to GND, central to 3.3V output, rightmost to 5V input. Place a 20 uF capacitor between 5V and GND, and a 10 uF between 3.3V (the output of AMS1117) and GND, in order to stabilize the voltage.

![](http://s17.postimg.org/jfk189ddr/ESp_12_E.png)



**Important**: to load things on the ESP, set GPIO0 to GND only when restarting/giving power/booting it up, then detach it, and it's in "load mode".
Make sure to have the proper driver for CP2102 usb to uart device for windows installed: https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers

Make sure to set WiFi credentials correctly in `src/secret_settings.h`.

Then, once platformio is installed (python2 only `:(` ), move into the hw directory and run: `pio run -t upload`.

To read the output from the serial on the terminal use: `pio device monitor -b 115200`.

To compile, load and see the output on the terminal with a single command: `pio run -t upload && pio device monitor -b 115200` on a terminal with bash support (like the one installed with Git on windows).