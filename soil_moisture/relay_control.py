import requests

def control(url, status):
    print(f"Control relay status {status}")
    param = {"relay": status}

    requests.get(url=url, params=param)

def relay_control(url, connection, relay):
    relay.off()
    relay_status = False

    while True:
        button = connection.get_sensor_boolean_value(1)

        if button == relay_status:
            continue

        if button:
            control(url, True)
            relay_status = True
        else:
            control(url, False)
            relay_status = False