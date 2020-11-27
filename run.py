import json
import paho.mqtt.client as paho
import requests

# MQTT broker setting
broker_url = "localhost"
broker_port = 1883
broker_timeout = 30
broker_username = "user"
broker_password = "password"


def on_connect(mqttc, userdata, flags, rc):
    if rc == 0:
        print("Connected With Result Code: {}".format(rc))
    else:
        print("Error! Not connected to broker.")


def on_disconnect(mqttc, userdata, rc):
    print("Client Got Disconnected")


# MQTT handler
mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.username_pw_set(username=broker_username, password=broker_password)
mqttc.connect(broker_url, broker_port, broker_timeout)


# Topic 2 - device2/topic2
def on_message_topic2(mosq, obj, msg):
    print("-------------------------")
    print("-------------------------")
    print("-------------------------")
    print("Topic: " + msg.topic)
    print("Message payload: ", msg.payload)
    payload = msg.topic

    service = 'modbus_rtu'
    match = ['rubix', 'points', service]
    t_parts = payload.split("/")
    point_name = None
    point_val = None
    point_fault = None
    if t_parts[0:3] == match and len(t_parts) == 10:
        try:
            point_name = t_parts[8]
            x = json.loads(msg.payload.decode('utf-8'))
            point_val = str("%s" % x['value'])
            point_fault = str("%s" % x['fault'])
        except Exception as e:
            print(e)
            pass
    #
    print("-------------------------")
    print(point_name)
    print(point_val)
    print(point_fault)
    print("-------------------------")

    ip = "0.0.0.0"
    port = 1717

    try:
        if point_name is not None:
            url = f'http://{ip}:{port}/api/bacnet/points/name/{point_name}'
            body = {
                "priority_array_write": {
                    "_16": point_val
                },
            }
            print(url)
            print(body)
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r_p = requests.patch(f'{url}', data=json.dumps(body), headers=headers)
            r_json = r_p.json()
            print(r_json)

    except Exception as e:
        print(e)
        pass


main_topic = "rubix/points/cov/all/+/+/+/+/+/modbus_rtu"
mqttc.subscribe("rubix/points/cov/#")
mqttc.message_callback_add(main_topic, on_message_topic2)

# Run endless loop
mqttc.loop_forever()
