import os
import time
from time import strftime, gmtime
from datetime import datetime, timedelta
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import traceback

#Log file
path = "log.txt"

def log_error(error_msg, path):
    formatted_date = strftime("%d/%m/%y %H:%M:%S")

    if os.path.exists(path):
        fileStat = os.stat(path)
        fileCreationTime = datetime.fromtimestamp(fileStat.st_ctime)
        weekAgo = datetime.utcnow() - timedelta(days=7)

        if fileCreationTime < weekAgo:
            weekNumber  = strftime("%U", gmtime())
            newFilename = f"log_{weekNumber}.txt"
            os.rename(path, newFilename)

    if not os.path.exists(path):
        with open(path, 'w') as log_file:
            log_file.write("Data i godzina - Błąd\n")

    with open(path, 'a') as log_file:
        log_file.write(f"{formatted_date} - {error_msg}\n")

#Room
roomTemperature = 0.0
roomHumidity    = 0.0
batteryVoltage  = 0.0
batteryPercent  = 0.0
#batteryLevelLow = False

def parseMagicESP(jsonBody):
    temp = jsonBody["DHT11"]["Temperature"]
    hum  = jsonBody["DHT11"]["Humidity"]
    return [temp, hum]

def parseESPSmartTermo(jsonBody):
    temp = jsonBody["Temperature"]
    hum  = jsonBody["Humidity"]
    vol  = jsonBody["BatteryVoltage"]
    per  = jsonBody["BatteryPercent"]
    #batL = jsonBody["BatteryLevelLow"] 
    return [temp, hum, vol, per]
    #return [temp, hum, vol, per, batL]

#CPU
cpuTemp = 0.0

def readCPUtemperature():
    with os.popen("cat /sys/class/thermal/thermal_zone0/temp") as terminal:
        temp = int(terminal.read()) / 1000.0
    return temp

def getUsedRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            RAMstats = line.split()[1:4]
            break
    return round(int(RAMstats[1]) / 1000,1)

def publishCPUData():
    cpuTemp = readCPUtemperature()
    mqttClient.publish(topic + "/CPU", cpuTemp)
    jsonCPUtemperature = createJSONbody("malinaCPUtemperature", cpuTemp, "MalinaTimeMachine")
    dbClient.write_points(jsonCPUtemperature)
    #print(f"CPU temperature {cpuTemp} C")

    usedRAM = getUsedRAMinfo()
    mqttClient.publish(topic + "/Used RAM", usedRAM)
    jsonCPUusedRAM = createJSONbody("malinaUsedRAM", usedRAM, "MalinaTimeMachine")
    dbClient.write_points(jsonCPUusedRAM)
    #print(f"Used RAM {usedRAM} MB")

#MQTT
username = "MQTT name"
password = "passoword"
broker   = "ip_addres"
topic    = "topic"
flagNewMessage = "Null"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # client.subscribe("malina/CPU")
    client.subscribe("tele/MagicESP/SENSOR")
    client.subscribe("ESP_Smart_Termo/ESP_ST1/Output")
    client.subscribe("ESP_Smart_Termo/ESP_ST2/Output")
    client.subscribe("ESP_Smart_Termo/ESP_ST3/Output")

def on_message(client, userdata, msg):
    global roomTemperature
    global roomHumidity
    global batteryVoltage
    global batteryPercent
    global flagNewMessage

    print("---- New message! ----")
    print("Time: " + strftime("%d/%m/%y %H:%M:%S") + " on topic: " + msg.topic)

    if (msg.topic == "tele/MagicESP/SENSOR"):
        measurements = parseMagicESP(json.loads(msg.payload)) 
        flagNewMessage = "MagicESP"

    if (msg.topic == "ESP_Smart_Termo/ESP_ST1/Output"):
        measurements = parseESPSmartTermo(json.loads(msg.payload)) 
        batteryVoltage = measurements[2]
        batteryPercent = measurements[3]
        flagNewMessage = "ESP_ST1"

    if (msg.topic == "ESP_Smart_Termo/ESP_ST2/Output"):
        measurements = parseESPSmartTermo(json.loads(msg.payload)) 
        batteryVoltage = measurements[2]
        batteryPercent = measurements[3]
        flagNewMessage = "ESP_ST2"

    if (msg.topic == "ESP_Smart_Termo/ESP_ST3/Output"):
        measurements = parseESPSmartTermo(json.loads(msg.payload)) 
        batteryVoltage = measurements[2]
        batteryPercent = measurements[3]
        flagNewMessage = "ESP_ST3"

    roomTemperature = measurements[0]
    roomHumidity    = measurements[1]

mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.username_pw_set(username, password)
mqttClient.connect(broker, 1883, 60)

#InfluxDB
influxdb_user     = "Database user"
influxdb_password = "passoword"
influxdb_host     = "ip_addres"
influxdb_port     = 1234
influxdb_database = "database_name"

dbClient = InfluxDBClient(influxdb_host, influxdb_port, influxdb_user, influxdb_password, influxdb_database)

def createJSONbody(measurement, value, room):
    if (value == 0):
        print ("Zero!")
        jsonBody = [
            {
                "measurement": measurement,
                "tags": {"room": room, "zero": "zero"},
                "fields": {"value": value}
            }
        ]
    else:
        jsonBody = [
            {
                "measurement": measurement,
                "tags": {"room": room},
                "fields": {"value": value}
            }
        ]
    return jsonBody

def createPayloadFromESPSmartTermo(name, rt, rh, bv, bp):
    jsonRoomTemperature = createJSONbody("roomTemperature", float(rt), name)
    jsonRoomHumidity    = createJSONbody("roomHumidity",    float(rh), name)
    jsonBatteryVoltage  = createJSONbody("batteryVoltage",  float(bv), name)
    jsonBatteryPercent  = createJSONbody("batteryPercent",  float(bp), name)
    return [jsonRoomTemperature, jsonRoomHumidity, jsonBatteryVoltage, jsonBatteryPercent]

def sendPayloadToDataBase(payload):
    for pl in range(len(payload)):
        dbClient.write_points(payload[pl])

# ---- main ----

#Loop
mqttClient.loop_start()

print("Hello!")

previous_time = time.time()
interval = 10

while True:
    try:
        if (flagNewMessage != "Null"):
            print("Flag: " + str(flagNewMessage))

        if ((flagNewMessage == "ESP_ST1") or (flagNewMessage == "ESP_ST2") or (flagNewMessage == "ESP_ST3")):
            if ((roomHumidity < 1.0) or (roomHumidity > 100.0) or (roomTemperature < 0.1)): #Bad way od solving problems 
                print("Bad sensor reading")
            else: 
                payload = createPayloadFromESPSmartTermo(flagNewMessage, float(roomTemperature), float(roomHumidity), float(batteryVoltage), float(batteryPercent))
                sendPayloadToDataBase(payload)
                print(f"ESP temp: {roomTemperature}C, hum: {roomHumidity}%, bat: {batteryVoltage} ({batteryPercent}%)")
                flagNewMessage = "Null"

        if (flagNewMessage == "MagicESP"):
            if ((roomHumidity < 1.0) or (roomHumidity > 100.0) or (roomTemperature < 0.1)): #Bad way od solving problems 
                print("Bad sensor reading")
            else: 
                jsonRoomTemperature = createJSONbody("roomTemperature", roomTemperature, "main_room")
                jsonRoomHumidity    = createJSONbody("roomHumidity",    roomHumidity,    "main_room")
                sendPayloadToDataBase([jsonRoomTemperature, jsonRoomHumidity])
                # dbClient.write_points(jsonRoomTemperature)
                # dbClient.write_points(jsonRoomHumidity)
                print(f"Room temp: {roomTemperature}, hum: {roomHumidity}")
                flagNewMessage = "Null"
        
        currentTime = time.time()
        if (currentTime - previous_time >= interval):
            publishCPUData()
            previous_time = currentTime

        time.sleep(0.1)

    except IOError as e:
        print("Błąd sieci! Oczekiwanie na wznowienie połączenia")

        error_msg = f"Błąd: {str(e)}\n{traceback.format_exc()}"
        # log_error(error_msg, path)

        time.sleep(10)

    except KeyboardInterrupt:
        #Close MQTT
        mqttClient.loop_stop()
        mqttClient.disconnect()
        print("\nMQTT disconnected")

        #Close InfluxDB
        dbClient.close()
        print("InfluxDB disconnected")

        log_error("Przerwanie klawiatury.", path)

        break

    except Exception as e:
        error_msg = f"Błąd: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        # log_error(error_msg, path)
        log_error("Błąd sieci", path)

    except InfluxDBServerError as e:
        error_msg = f"Błąd: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        # log_error(error_msg, path)
        log_error("Influx ma problem", path)

