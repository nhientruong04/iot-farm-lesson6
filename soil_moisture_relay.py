import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_relay import GroveRelay

from cloud import IoTHub

CounterFitConnection.init('127.0.0.1', 5000)

TOPIC = 'counterfit/relay'
CERTIFICATES_DIR = "certs_test2"
ENDPOINT = "a1zavzvofzdchy-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "test2_device"
PATH_TO_CERTIFICATE = "certs_test2/test2-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs_test2/test2-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs_test2/AmazonRootCA1.pem"
iot_hub = IoTHub(
    endpoint=ENDPOINT,
    client_id=CLIENT_ID,
    cert_path=PATH_TO_CERTIFICATE,
    private_key_path=PATH_TO_PRIVATE_KEY,
    root_ca_path=PATH_TO_AMAZON_ROOT_CA_1
)

iot_hub.connect()
iot_hub.subscribe_cloud(TOPIC)

relay = GroveRelay(5)
count = 0
while count<10:
    relay_on = False

    # print("Soil moisture:", soil_moisture)

    # if soil_moisture > 450:
    #     relay_on = True
    #     telemetry = json.dumps({'relay_on' : relay_on})
    #     # mqtt_client.publish(client_telemetry_topic, telemetry)
    # else:
    #     relay_on = False
    #     telemetry = json.dumps({'relay_on' : relay_on})
    #     # mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
    count += 1

iot_hub.disconnect()