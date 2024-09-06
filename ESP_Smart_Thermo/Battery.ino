float readBatteryVoltage() {
  // const float adcFactor = 0.00549538;
  float adcValue;
  float voltage;

  adcValue = analogRead(adcPin);
  // voltage = (adcValue * adcFactor);
  voltage = (adcValue / 1023) * 4.2;

  Serial.print("Battery voltage: "); 
  Serial.print(voltage); 
  Serial.println(" V");
  return voltage;
}

float batteryMap(float batteryVoltage) {
  float batteryPercentage = mapFloat(batteryVoltage, 3.3, 4.2, 0.0, 100.0);
 
  if (batteryPercentage >= 100.0) {
    batteryPercentage = 100.0;
  }
  if (batteryPercentage <= 0.0) {
    batteryPercentage = 0.0;
  }

  Serial.print(F("Battery percent: ")); Serial.print(batteryPercentage); Serial.println(F("%"));
  return batteryPercentage;
}

float mapFloat(float input, float in_min, float in_max, float out_min, float out_max) {
  return (input - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}