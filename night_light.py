import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_connection import CounterFitConnection
import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5000)

id = 'd2ba7ebd-3a21-4066-aa44-59fc3488016b'
client_name = id + 'nightlight_client'
client_telemetry_topic = id + '/telemetry'

light_sensor = GroveLightSensor(0)

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light' : light})
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(2)