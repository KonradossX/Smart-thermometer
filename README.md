# About

I designed my own PCB based on the ESP-12 (ESP8266) and DHT11 sensor to measure room temperature and humidity. Measurements are sent via Wi-Fi using MQTT to a broker running on a Raspberry Pi. From the MQTT broker, my custom code downloads, parses, and saves the measurements in an Influx database. Historical data is displayed using Grafana. After each measurement and successful transmission, the board enters deep sleep for 10 minutes to conserve battery life. Additionally, through HomeBridge, the data from MQTT is forwarded to an iPhone.

## Features

- 3 custom-designed boards with my own code
- 1 development board with Tasmota (Sonoff) firmware
- Apple HomeKit integration via HomeBridge using the Mqttthing plugin
- Grafana data visualization
- InfluxDB for data storage
- Raspberry Pi server (for running InfluxDB, Grafana, and handling data reading and saving)

## Prerequisites
- ESP-12 (ESP8266)
- DHT11 sensor
- Raspberry Pi
- MQTT broker (e.g., Mosquitto)
- InfluxDB and Grafana installed on Raspberry Pi
- HomeBridge and Mqttthing plugin for HomeKit integration
- Wi-Fi network credentials
- Basic programming knowledge (for editing code and configuration files)

## Related

Circuit design and project inspiration from:

[how2electronics.com](https://how2electronics.com/design-your-own-esp-board-for-battery-powered-iot-applications/)

## Authors

- [@KonradossX](https://www.github.com/KonradossX)

## Screenshots

![Grafana](https://github.com/KonradossX/Smart-thermometer/blob/main/Screens%20and%20photos/grafana.png?raw=true)

![iPhone](https://github.com/KonradossX/Smart-thermometer/blob/main/Screens%20and%20photos/iPhone%20%201.jpg?raw=true)

![iPhone](https://github.com/KonradossX/Smart-thermometer/blob/main/Screens%20and%20photos/iPhone%20%202.jpg?raw=true)
