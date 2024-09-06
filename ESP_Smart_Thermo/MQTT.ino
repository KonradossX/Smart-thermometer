//Connect to MQTT broker
const char* mqttUser     = "MQTT name";
const char* mqttPassword = "password";

void mqttConnect() {
  while(!client.connected()) {
    if (client.connect(mqttName, mqttUser, mqttPassword)) {
      // client.publish(mqttTopicOut, "hello world");
      client.subscribe(mqttTopicIn);
      Serial.println("MQTT connected!");
    } else {
      Serial.print("Failed MQTT connecton");
      Serial.print(client.state());
      blink(5, 250, 250);
    }
  }
}

void sendStatusMessage(String statusMessage) {
  statusMessage.toCharArray(charsToSend, statusMessage.length() + 1);
  client.publish(mqttTopicStatus, charsToSend);
}

void callback(char* topic, byte* payload, unsigned int length) {
  //blink(3, 100, 100);
  String messageTemp;

  Serial.print("Message: >>");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    messageTemp += (char)payload[i];
  }
  Serial.println("<<");

  if (String(topic) == mqttTopicIn) {
    Serial.println("LED");
    if (messageTemp == "OFF") {
      digitalWrite(LedPin, HIGH);
      Serial.println("OFF");
    }

    if (messageTemp == "ON") {
      digitalWrite(LedPin, LOW); 
      Serial.println("ON");
    }
  }
}

// //Make mqtt path and topic 
// char* makeTopicCharArray(char* path) {
//   char* topic;
//   strcat(topic, mqttTopic);
//   strcat(topic, path);
//   return topic;
// }