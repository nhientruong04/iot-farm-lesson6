# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json


def handle_telemetry(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic {topic}")
    print(f"Received payload {payload}")
    # payload = json.loads(message.payload.decode())
    # relay_on = payload['relay_on']
    # print("Message received:", relay_on)

    # if relay_on:
    #     relay.on()
    # else:
    #     relay.off()

class IoTHub():
	def __init__(self, endpoint, client_id, cert_path, private_key_path, root_ca_path):
		self.event_loop_group = io.EventLoopGroup(1)
		self.host_resolver = io.DefaultHostResolver(self.event_loop_group)
		self.client_bootstrap = io.ClientBootstrap(self.event_loop_group, self.host_resolver)
		self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
				endpoint=endpoint,
				cert_filepath=cert_path,
				pri_key_filepath=private_key_path,
				client_bootstrap=self.client_bootstrap,
				ca_filepath=root_ca_path,
				client_id=client_id,
				clean_session=False,
				keep_alive_secs=5
		)

	def subscribe_cloud(self, sub_topic):
		self.subscribe_future, _ =  self.mqtt_connection.subscribe(
										topic=sub_topic,
										qos=mqtt.QoS.AT_LEAST_ONCE,
										callback=handle_telemetry)

		return self.subscribe_future.result()

	def publish_cloud(self, payload, topic):
		# Make the connect() call
		
		# Future.result() waits until a result is available
		self.mqtt_connection.publish(topic=topic, payload=json.dumps(payload), qos=mqtt.QoS.AT_LEAST_ONCE)
		print("Published: '" + json.dumps(payload) + "' to the topic: " + topic)

	def connect(self):
		self.connect_future = self.mqtt_connection.connect()
		
		return self.connect_future.result()

	def disconnect(self):
		self.disconnect_future = self.mqtt_connection.disconnect()

		return self.disconnect_future.result()