//WiFi 2,4G config
#define wifiSSID "SSID_WIFI"
#define wifiPassword "password"

//WiFi 5G config 
// #define wifissid     "UPC58768685"
// #define wifipassword "4J4N5CSK"

//Configure WiFi connection
void wifiSetup() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(wifiSSID, wifiPassword);
  //blink(3, 200, 200);
  
  while (WiFi.status() != WL_CONNECTED) {
    blink(1, 400, 100);
    Serial.print(".");
  }
  Serial.println("WIFI connected!");
  //blink(3, 200, 200);
}