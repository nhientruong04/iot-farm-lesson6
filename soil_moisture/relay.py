import time, json

global grove_relay

def handle_telemetry(topic, payload, dup, qos, retain):
    global grove_relay

    message = json.loads(payload)
    print(f"Received message {message} from topic {topic}")

    relay_on = message['relay']

    if relay_on:
        grove_relay.on()
    else:
        grove_relay.off()


def relay_thread(iot_hub, sub_topic, relay):
    global grove_relay
    grove_relay = relay

    iot_hub.subscribe_cloud(sub_topic=sub_topic, on_message_handle=handle_telemetry)

    while True:
        time.sleep(2)