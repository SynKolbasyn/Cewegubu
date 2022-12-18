import paho.mqtt.client as mqttclient
import time

message_received = False
connected = False

brokerAdress = "mqtt.by"
port = 1883
user = "synkolbasyn"
password = "fhyeonco"
topic_save = "/user/synkolbasyn/gamedata"
topic_for_command = "/user/synkolbasyn/command"
topic_from_server = "/user/synkolbasyn/fromdata"
text = ""
command = "saveData"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # print("client is connected")
        global connected
        connected = True
    else:
        connected = False
        # print("connection failed")


def on_message(client, userdata, message):
    b = 0
    message_received = True
    # print("message recieved", str(message.payload.decode("utf-8")))
    # print("topic", str(message.topic))
    global text
    try:
        text = str(message.payload.decode("utf-8"))
    except UnicodeDecodeError:
        b = 1


def uploadText(topic, text):
    '''Отправляет  текст в указанный топик'''
    client = mqttclient.Client("MQTT")
    client.username_pw_set(user, password=password)
    client.on_connect = on_connect
    client.connect(brokerAdress, port=port)

    # message_received = False
    # connected = False

    client.loop_start()
    while connected != True:
        time.sleep(0.2)
    client.publish(topic, text)
    client.loop_stop()


def downloadText(topic):
    '''Читает сообщение с указанного топика'''
    message_received = True
    # connected = False
    client = mqttclient.Client("MQTT")
    client.on_message = on_message
    client.username_pw_set(user, password=password)
    client.connect(brokerAdress, port=port)
    client.on_connect = on_connect
    client.subscribe(topic)

    client.loop_start()
    while connected != True:
        time.sleep(0.2)
    while message_received != True:
        # time.sleep(0.2)
        if text != "":
            message_received = True
    client.loop_stop()
    return text

def serverAnswer():
    a = downloadText("/user/synkolbasyn/gamedata")
    oldA = ""
    while True:
        message_received = False
        connected = False
        a = downloadText("/user/synkolbasyn/gamedata")
        if a != "" and a != oldA:
            oldA = a