import time

def sensor_thread(iot_hub, pub_topic, sensor):
    while True:
        soil_moisture = sensor.read(0)
        payload = {"soil-moisture": soil_moisture}
        iot_hub.publish_cloud(payload, pub_topic)

        time.sleep(5)