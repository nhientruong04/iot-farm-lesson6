import time
from counterfit_shims_grove.adc import ADC
import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay
import json

CounterFitConnection.init('127.0.0.1', 5000)

id = 'd2ba7ebd-3a21-4066-aa44-59fc3488016b'
client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/soil_moisture'

adc = ADC()
relay = GroveRelay(5)

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    relay_on = payload['relay_on']
    print("Message received:", relay_on)

    if relay_on:
        relay.on()
    else:
        relay.off()

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    relay_on = False
    soil_moisture = adc.read(0)
    print("Soil moisture:", soil_moisture)

    if soil_moisture > 450:
        relay_on = True
        telemetry = json.dumps({'relay_on' : relay_on})
        mqtt_client.publish(client_telemetry_topic, telemetry)
    else:
        relay_on = False
        telemetry = json.dumps({'relay_on' : relay_on})
        mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)