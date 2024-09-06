void blink(int number, int timeON, int timeOFF) {
  bool prevState;
  prevState = digitalRead(LedPin);

  for (int i = 0; i < number; i++) {
    digitalWrite(LedPin, HIGH);
    delay(timeON);
    digitalWrite(LedPin, LOW);
    delay(timeOFF);
  }

  digitalWrite(LedPin, prevState);
}

String createJSONmsg(float tempV, float humidityV, float batVoltage, float batPercent, bool batLow) {
  String outputJSON;
  StaticJsonDocument<64> doc;

  doc["Temperature"]    = tempV;
  doc["Humidity"]       = humidityV;
  doc["BatteryVoltage"] = batVoltage;
  doc["BatteryPercent"] = batPercent;
  doc["BatteryLow"]     = batLow;

  serializeJson(doc, outputJSON);
  return outputJSON;
}

