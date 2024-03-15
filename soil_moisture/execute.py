import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from counterfit_connection import CounterFitConnection
from threading import Thread
from sensor import sensor_thread
from relay import relay_thread

from cloud import IoTHub

CounterFitConnection.init('127.0.0.1', 5000)

PUB_TOPIC = 'counterfit/sensor'
SUB_TOPIC = 'counterfit/relay'
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
adc = ADC()
relay = GroveRelay(5)

threading_relay = Thread(target=relay_thread, kwargs={"iot_hub": iot_hub, "sub_topic": SUB_TOPIC, "relay": relay}, daemon=True)
threading_sensor = Thread(target=sensor_thread, kwargs={"iot_hub": iot_hub, "pub_topic": PUB_TOPIC, "sensor": adc}, daemon=True)

try:
    print("Starting sensor thread.")
    threading_sensor.start()
    
    print("Starting relay thread.")
    threading_relay.start()

    threading_sensor.join()
    threading_relay.join()

except KeyboardInterrupt:
    print("\nProcess killed")
    