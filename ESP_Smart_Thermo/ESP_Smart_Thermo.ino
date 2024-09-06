//Libraries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

//Config
#define refreshTime 600000000 //10 min
// #define refreshTime 300000000 //5 min
//#define refreshTime 60000000 //1min
//#define refreshTime 100000 //ms
#define DHTTYPE DHT11
#define DHTPIN 13
#define LedPin 2
#define adcPin A0
#define batteryLevelLow 25.0
#define batteryLevelDead 10.0

//MQTT
#define mqttPort              1234
const char* mqttIP          = "ip_addres";
const char* mqttName        = "ESP_ST1";
const char* mqttTopicOut    = "ESP_Smart_Termo/ESP_ST1/Output";
const char* mqttTopicIn     = "ESP_Smart_Termo/ESP_ST1/Input";
const char* mqttTopicStatus = "ESP_Smart_Termo/ESP_ST1/Status";
#define MSG_BUFFER_SIZE	(50)

//Define 
WiFiClient espClient;
PubSubClient client(espClient);
DHT_Unified dht(DHTPIN, DHTTYPE); 

unsigned long lastMsgTime = 0;
char msgText[50];
//int value = 0;
char charsToSend[100];
String messageToSend;

//Flags
bool errorDHT = false;

void setup() {
  Serial.begin(9600);
  Serial.println("\nHello world!");

  dht.begin();
  dhtSensorData();

  wifiSetup();
  client.setServer(mqttIP, mqttPort);
  client.setCallback(callback);
  
  pinMode(LedPin, OUTPUT);
  digitalWrite(LedPin, LOW);

  if (!client.connected()) {
    mqttConnect();
  }
  sendStatusMessage("Awake");
}

void loop() {
  if (!client.connected()) {
    mqttConnect();
  }
  client.loop();

  float t, h, bv, bp;
  bool bl; //battery low
  unsigned long nowTime = millis();
  //Serial.println(nowTime);

  //if (nowTime - lastMsgTime > refreshTime) {
  if (true == true) {
    lastMsgTime = nowTime;
    //++value;
    Serial.println("Now");
    // snprintf (msgText, MSG_BUFFER_SIZE, "hello mqtt #%ld", value);
    // Serial.print("Publish message: ");
    // Serial.println(msgText);
    // client.publish(mqttTopicOut, msgText);

    t = readTemperature();
    h = readHumidity();
    bv = readBatteryVoltage();
    bp = batteryMap(bv);

    if (bp < batteryLevelLow)
      bl = true;
    else
      bl = false;

    messageToSend = createJSONmsg(t, h, bv, bp, bl);
    // charsToSend[messageToSend.length() + 1];
    messageToSend.toCharArray(charsToSend, messageToSend.length() + 1);
    client.publish(mqttTopicOut, charsToSend);

    if (errorDHT == true) {
      sendStatusMessage("Error reading DHT11!");
      errorDHT = false;
    }

    goSleep(bp);
  }

  //Serial.print(".");
}

