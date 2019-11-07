import face_recognition as citra
import paho.mqtt.client as mqtt
import requests
import pymongo
import json
import fungsi_publish as pub

BROKER_ADDRESS = '192.168.43.201'
MQTT_PORT = 1883
MQTT_TOPIC = 'jarak1'

def on_connect(client, userdata, flags, rc):
    print('Connected with result code',  str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    print(payload)
    jarak=float(payload)
    if(jarak<30):
        print("panggil fungsi recog")
        statusservo=citra.fungsirecognetion()
        print(statusservo)
        client.connect(BROKER_ADDRESS, MQTT_PORT, 60)
        print("publishing message to topic")
        client.publish("servo",statusservo)
    else:
        print("tidak ada orang")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, MQTT_PORT, 60)
    client.loop_forever()
