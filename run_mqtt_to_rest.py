import json
import paho.mqtt.client as paho
import requests

# MQTT broker setting
broker_url = "localhost"
broker_port = 1883
broker_timeout = 30
broker_username = "user"
broker_password = "password"
DEBUG = False


def on_connect(mqttc, userdata, flags, rc):
    if rc == 0:
        if DEBUG:
            print("Connected With Result Code: {}".format(rc))
    else:
        if DEBUG:
            print("Error! Not connected to broker.")


def on_disconnect(mqttc, userdata, rc):
    if DEBUG:
        print("Client Got Disconnected")


# MQTT handler
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.connect(broker_url, broker_port, broker_timeout)


def on_message_topic2(mosq, obj, msg):
    payload = msg.topic
    service = 'cov'
    match = ['rubix', 'points', service]
    t_parts = payload.split("/")
    point_name = None
    point_val = None
    point_fault = None
    if t_parts[0:3] == match and len(t_parts) == 11:
        try:
            point_name = t_parts[5]
            x = json.loads(msg.payload.decode('utf-8'))
            point_val = str("%s" % x['value'])
            point_fault = str("%s" % x['fault'])
        except Exception as e:
            if DEBUG:
                print(e)
            pass

    ip = "0.0.0.0"
    port = 1717
    try:
        url = f'http://{ip}:{port}/api/bacnet/points/name/{point_name}'
        body = {
            "priority_array_write": {
                "_16": point_val
            },
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r_p = requests.patch(f'{url}', data=json.dumps(body), headers=headers)
        r_json = r_p.json()
        if DEBUG:
            print(r_json)


    except Exception as e:
        if DEBUG:
            print(e)
        pass


"rubix/points/cov/all/ec6cf0a5-95b9-47c0-bd2f-927331ef23ff/mode_18_6/1177f4f8-b229-41c8-92b3-3a259a7f2fc9/device_18/fd663f30-06f9-436c-851f-693a5a34011c/mod_network_name hey/modbus_rtu"
"rubix/points/cov/all/+/mode_18_6/+/device_18/+/+/modbus_rtu"
# main_topic = "rubix/points/cov/all/#"
main_topic = "rubix/points/cov/all/+/+/+/+/+/+/modbus_rtu"
mqttc.subscribe("rubix/points/cov/all/#")
mqttc.message_callback_add(main_topic, on_message_topic2)

# Run endless loop
mqttc.loop_forever()
