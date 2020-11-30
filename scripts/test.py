import datetime
import psycopg2
import paho.mqtt.client as mqtt

MQTT_ADDRESS = '0.0.0.0'
CONNECTION = "postgres://postgres:postgres@0.0.0.0/bac_rest"
DEBUG = True
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe('test/temp')


def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    if DEBUG:
        print(msg.topic + ' ' + str(float(msg.payload.decode("utf-8"))))
    if msg.topic == 'test/temp':
        device_id = 'aasd'
        client_id = 'asd'
        point = 'dev-1234345'
        ts = str(datetime.datetime.now())
        val = float(msg.payload.decode("utf-8"))

        if DEBUG:
            print({
                'device_id': device_id,
                'client_id': client_id,
                'point': point,
                'ts': ts,
                'val': val,
            })
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


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to DB bridge')
    main()
