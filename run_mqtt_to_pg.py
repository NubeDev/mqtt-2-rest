import paho.mqtt.client as paho
import psycopg2
import datetime
import configparser
import os

DEBUG = False

temp_path = os.path.dirname(os.path.abspath(__file__))
part_config = os.path.join(temp_path, "config.ini")
config = configparser.ConfigParser()
config.read(part_config)

# MQTT broker setting
broker_url = config.get("mqtt", "broker")
broker_port = int(config.get("mqtt", "mqtt_port"))
main_topic = config.get("pg", "main_topic")
point_topic = config.get("pg", "point_topic")
broker_timeout = 30
broker_username = "user"
broker_password = "password"
CONNECTION = config.get("pg", "server")
# CONNECTION = "postgres://postgres:postgres@0.0.0.0/bac_rest"

conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()


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
mqttc.connect(broker_url, broker_port, broker_timeout)


def on_message_topic2(mosq, obj, msg):
    payload = msg.topic
    service = 'pg'
    match = ['rubix', service]
    t_parts = payload.split("/")
    device_id = 'aasd'
    client_id = 'asd'
    point = None
    ts = None
    val = None

    if t_parts[0:2] == match and len(t_parts) == 3:
        try:
            point = t_parts[2]
            ts = str(datetime.datetime.utcnow())
            val = float(msg.payload.decode("utf-8"))
        except Exception as e:
            print(e)
            pass
        try:
            conn = psycopg2.connect(CONNECTION)
            query = """ INSERT INTO histories (deviceid, clientid, point, ts, val)
                          VALUES (%s,%s,%s,%s,%s)"""
            values = (device_id, client_id, point, ts, val)
            with conn:
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()

        except Exception as e:
            print(e)
            pass


mqttc.subscribe(main_topic)
mqttc.message_callback_add(point_topic, on_message_topic2)

# Run endless loop
mqttc.loop_forever()
