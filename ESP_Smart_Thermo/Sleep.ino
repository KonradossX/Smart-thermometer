void goSleep(float batteryLevel) {
  Serial.print("Battery level: ");
  Serial.println(batteryLevel);
  Serial.println("Go sleep");

  int sleepTime;
  if (batteryLevel > batteryLevelLow) {
    sleepTime = refreshTime;
    sendStatusMessage("Sleep");
  } else if (batteryLevel < batteryLevelDead) {
    sleepTime = 0;
    //sleepTime = refreshTime * 1;
    sendStatusMessage("Dead battery");
  } else {
    sleepTime = refreshTime * 2;
    sendStatusMessage("Longer sleep");
  }

  Serial.print("Sleep time: ");
  Serial.println(sleepTime);
  Serial.println("End");

  delay(500);

  Serial.end();
  client.disconnect();
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  //dht.powerDown(); //not work

  digitalWrite(LedPin, HIGH); //Turn OFF LED
  delay(250);
  ESP.deepSleep(sleepTime);
}