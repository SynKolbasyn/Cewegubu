import re
from threading import Thread
import paho.mqtt.client as mqttclient
import time
import json
#
# word = "Hell08o "
# word = word.lower()
# print("|" + word + "|")
# print(re.search(r'[^a-z 0-9_]+', word))
# try:
#     re.search(r'[^a-z 0-9_]+', word).group(0)
#     print("ok")
# except AttributeError:
#     print("no")
#
# if re.search(r'[^a-z 0-9_]+', word) == None:
#     print("ok")
# else:
#     print("no")
#
# def a(b, c=0, d=0):
#     print(b)
#     print(c)
#     print(d)
#
# a(1,3,5)
#
# def gameBody():
#     print("hello")
#
# th1 = Thread(target=gameBody, args=())
# th2 = Thread(target=gameBody, args=())
# th1.start()
# th2.start()

message_received = False
connected = False

brokerAdress = ""
port =
user = ""
password = ""
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

# def save(game_data):
#     '''Отправляет команду в топик, после чего сохраняет данные "game_data"'''
#     # uploadText(topic_for_command, command)
#     uploadText(topic_save, game_data)
#
#
# def loadFromServer():
#     '''Загружает данные с сервера'''
#     text = downloadText(topic_from_server)
#     file = open("data/gameData.txt", 'w')
#     file.write(text)
#     file.close()
#     file = open("data/gameData.txt", 'r')
#     a = []
#     for line in file:
#         ta = []
#         ta = line.split("\t")
#         a.append(Character(ta[0].strip(),
#                            ta[1].strip(),
#                            ta[2].strip(),
#                            ta[3].strip(),
#                            ta[4].strip(),
#                            ta[5].strip(),
#                            ta[6].strip(),
#                            ta[7].strip(),
#                            ta[8].strip()))
#     file.close()
#     '''Удаляем содержимое файла'''
#     file = open("data/gameData.txt", 'w')
#     file.write("")
#     file.close()
#     return a


def encode(players):
    text = ""
    for i in players:
        text = text + \
               i.name + "\t" + \
               i.login + "\t" + \
               i.password + "\t" + \
               i.nickName + "\t" + \
               i.rass + "\t" + \
               i.money + "\t" + \
               i.exp + "\t" + \
               i.helthPoints + "\t" + \
               i.damage + "\n"
    return text

def saveToFileW(text):
    file = open("data/gameData.txt", 'w')
    file.write(text)
    file.close()

# while True:
#     d = 0
#     a = downloadText("/user/synkolbasyn/gamedata")
#     oldA = ""
#     while a == "":
#         message_received = False
#         connected = False
#         a = downloadText("/user/synkolbasyn/gamedata")
#         if a != "" and a != oldA:
#             print(d, a)
#             d += 1
#             oldA = a
#
#     f = open("gameData.json", "w")
#     a = a.replace('\n', '')
#     a = a.replace('\r', '')
#     # a = a.replace('\"', '"')
#     # a = ''.join([a[i] for i in range(len(a)) if i != 0])
#     a = a.replace(' ', '')
#     print(a)
#     # json.dump(a, f, indent=4)
#     f.write(a)
#     f.close()
#     c = ""
#     for i in open("gameData.json", "r"):
#         c += i
#     b = json.loads(c)
#     for i in range(b["players"]):
#         print(b["player"][i]["email"])
#     f = open("gameData.json", "w")
#     # f.write(json.dumps(b, indent=4))
#     json.dump(b, f, indent=4)
#     f.close()

c = ""
for i in open("gameData.json", "r"):
    c += i

uploadText("/user/synkolbasyn/forServer", c)