from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
from counterfit_connection import CounterFitConnection
from threading import Thread
from sensor import sensor_thread
from relay import relay_thread
import argparse
from relay_control import relay_control
from cloud import IoTHub

parser = argparse.ArgumentParser()
parser.add_argument('--relay_control', action='store_false', help='True if activate sensor and relay connection, False if activate relay connection and relay control module.')

args = parser.parse_args()

CounterFitConnection.init('127.0.0.1', 5000)

PUB_TOPIC = 'counterfit/sensor'
SUB_TOPIC = 'counterfit/relay'
ENDPOINT = "a1zavzvofzdchy-ats.iot.ap-southeast-1.amazonaws.com"
# CLIENT_ID = "test2_device"
# PATH_TO_CERTIFICATE = "certs_test2/test2-certificate.pem.crt"
# PATH_TO_PRIVATE_KEY = "certs_test2/test2-private.pem.key"
# PATH_TO_AMAZON_ROOT_CA_1 = "certs_test2/AmazonRootCA1.pem"

CLIENT_ID = "counterfit_off"
PATH_TO_CERTIFICATE = "certs_off/counterfit_official-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certs_off/counterfit_official-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certs_off/AmazonRootCA1.pem"

URL = 'https://p5gwvdut5ljvhwsmn2bhxw7a740vktax.lambda-url.ap-southeast-1.on.aws/'

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

try:
    if args.relay_control:
        print("Starting sensor and relay threads.")
        threading_relay = Thread(target=relay_thread, kwargs={"iot_hub": iot_hub, "sub_topic": SUB_TOPIC, "relay": relay}, daemon=True)
        threading_sensor = Thread(target=sensor_thread, kwargs={"iot_hub": iot_hub, "pub_topic": PUB_TOPIC, "sensor": adc}, daemon=True)
        threading_sensor.start()
        threading_relay.start()

        threading_sensor.join()
        threading_relay.join()

    else:    
        print("Starting relay and relay control threads.")
        threading_relay = Thread(target=relay_thread, kwargs={"iot_hub": iot_hub, "sub_topic": SUB_TOPIC, "relay": relay}, daemon=True)
        threading_relay_control = Thread(target=relay_control, kwargs={"url": URL, "connection": CounterFitConnection, "relay": relay}, daemon=True)
        threading_relay.start()
        threading_relay_control.start()

        threading_relay.join()
        threading_relay_control.join()

except KeyboardInterrupt:
    print("\nProcess killed")