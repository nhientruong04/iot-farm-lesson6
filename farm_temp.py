import time
import os, csv
from datetime import datetime
from counterfit_shims_seeed_python_dht import DHT
from counterfit_connection import CounterFitConnection
import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5000)

id = 'd2ba7ebd-3a21-4066-aa44-59fc3488016b'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'

temp_sensor = DHT("11", 5)

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']

if not os.path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    with open(temperature_file_name, mode='a') as temperature_file:        
        temperature_writer = csv.DictWriter(temperature_file, fieldnames=fieldnames)
        temperature_writer.writerow({'date' : datetime.now().astimezone().replace(microsecond=0).isoformat(), 'temperature' : payload['temp']})


mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    _, temp = temp_sensor.read()
    telemetry = json.dumps({'temp' : temp})
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(0.5)