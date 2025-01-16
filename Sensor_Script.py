import paho.mqtt.client as mqtt
import json
import socket
import time
from db.db_model import DBModel
import traceback

db = DBModel

# mqtt cridentials:
mqttHost = "127.0.0.1"
mqttPort = 1883

cameraHost = "10.0.0.45"
cameraPort = 2112

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.settimeout(5.0)
#clientsocket.connect((cameraHost, cameraPort))

def sendCommand(command):
    payload = '\x02{}\x03'.format(command)
    print('sending {}'.format(payload))

    clientsocket.send(payload.encode())
    clientsocket.settimeout(8.0)
    response = clientsocket.recv(1024)

    print("Sent {} and received {}".format(payload, response))
    if response.decode().strip().replace('\x02', '').replace('\x03', ''):
        print("Command executed successfully!")
        return True
    else:
        print("Received nothing")
        return False

# callback for connection attempt result
def on_connect(client, userdata, flags, rc,null):
    print("Connected with result code " + str(rc))

# callback for subscribing result
def on_subscribe(client, userdata, mid, reason_code_list, properties=None):
    if reason_code_list[0].is_failure:
        print("subscribe failed, rejected by broker")
    else:
        print("subscribe succeded")

def start_reading():
    sendCommand(21)

def stop_reading():
    sendCommand(22)

# callback for when you receive a message
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    if msg.topic == "get_position":
            start_interval = time.time()
            delay = 10

            #start_reading()
            reading = True
            while True:
                try:
                    # clientsocket.settimeout(8.0)
                    # response = clientsocket.recv(1024)
                    # print(response)
                    # response = response.decode().strip().replace('\x02', '').replace('\x03', '')
                    # print('found code:{}'.format(response))
                    # stop_reading()
                    res = dict()
                    res["pos"] = 7
                    mqttc.publish("position", json.dumps(res), qos=2, retain=True)
                    break
                except TimeoutError:
                    print('nothing received for 5s')


# subscribes to the given topic
# (optional) topic can be cleared before subscribing by setting cleartopic to true
def mqttSubscribe(topic, cleartopic=False):
    if cleartopic:
        mqttc.publish(topic, payload="", retain=True)
    mqttc.subscribe(topic, qos=2)
    print("subscribing to " + topic)

# publishes to a topic
def mqttPublish(topic, payload, qos=2, retain=False):
    mqttc.publish(topic=topic, payload=payload, qos=qos, retain=retain)

if __name__ == "MQTT":
   mqttc.on_connect = on_connect
   mqttc.on_message = on_message
   mqttc.on_subscribe = on_subscribe

   # this sets up the connections with the mqtt server
   mqttc.connect(mqttHost, port=mqttPort)

   mqttSubscribe(
       topic="get_position",
       cleartopic=True
    )

   mqttc.loop_forever()

if __name__ == "__main__":

    while True:

        r = input("Start Read Y/N").lower()
        if r == 'y':
            start_reading()

            try:
                code = clientsocket.recv(1024)

                print(f'Received Repsonse: {code}')


            except:

                print(f'Exception while reading')
                traceback.print_exc()

        if r == 'exit':
            stop_reading()
            break

    print('Program finished succesfully')

