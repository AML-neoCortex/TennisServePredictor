# Tennis Serve Predictor

| Team neoCortex |
| --- | 
| Sacha Hakim |
| Noan Le Renard |
| Hazem Masoud |
| Michal Makowka |
| Antonios Papaoikonomou |

---
## Prerequisites:

### Software & System Drivers Required
1. Download Arduino: 
https://www.arduino.cc/en/software
2. Install CH340 USB -> Serial drivers: 
https://learn.sparkfun.com/tutorials/how-to-install-ch340-drivers/all

If you don't follow the above, the board will not be recognised by Windows Device Manager.

---
## Arduino Packages
A number of boards and libraries is required for firmware development.

Open ARDUINO CC.

Enter **FILE -> PREFERENCES -> SETTINGS** and copy below into **Additional Boards Manager URLs**:

`https://raw.githubusercontent.com/DFRobot/FireBeetle-ESP8266/master/package_firebeetle8266_index.json`
	
Search additional boards and install **FireBeetle-ESP32 Mainboard by DFRobot**

Then once again enter **FILE -> PREFERENCES -> SETTINGS** and copy below into **Additional Boards Manager URLs**:

`https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
	
Install **esp32 by Espressif Systems** board.

These will also load and install relevant example sketches.

---

Now, regardless of the additional URLs set, search and install the following librarires:

1. **Adafruit BNO055 by Adafruit** library. When prompted, install **Adafruit Unified Sensors System** as well! This will happen automatically.
2. **Adafruit NeoPixel by Adafruit** library. This one is needed to control three WS2812B LEDs fitted on the IMU module.

