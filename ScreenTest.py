# To learn how to drive the Screen
#  This is 192.168.1.230
#

import TouchScreen
import serial
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import queue
import time
import uuid


cbuslamps = {"16": {'name': 'Porch',    'lamp_x':  '10', 'lamp_y': '275', 'label_x':  '45', 'label_y': '265', 'level': 2, 'chnged': 'N'},
             "14": {'name': 'Entrance', 'lamp_x':  '70', 'lamp_y': '275', 'label_x': '105', 'label_y': '265', 'level': 2, 'chnged': 'N'},
             "15": {'name': 'Study',    'lamp_x': '130', 'lamp_y': '275', 'label_x': '165', 'label_y': '265', 'level': 2, 'chnged': 'N'},
             "12": {'name': 'Master',   'lamp_x': '190', 'lamp_y': '275', 'label_x': '225', 'label_y': '265', 'level': 2, 'chnged': 'N'},
             "13": {'name': 'Lounge',   'lamp_x':  '10', 'lamp_y': '211', 'label_x':  '45', 'label_y': '201', 'level': 2, 'chnged': 'N'},
             "0A": {'name': 'Passage',  'lamp_x':  '70', 'lamp_y': '211', 'label_x': '105', 'label_y': '201', 'level': 2, 'chnged': 'N'},
             "11": {'name': 'Bathroom', 'lamp_x': '130', 'lamp_y': '211', 'label_x': '165', 'label_y': '201', 'level': 2, 'chnged': 'N'},
             "10": {'name': 'Toilet',   'lamp_x': '190', 'lamp_y': '211', 'label_x': '225', 'label_y': '201', 'level': 2, 'chnged': 'N'},
             "0C": {'name': 'Dining',   'lamp_x':  '10', 'lamp_y': '147', 'label_x':  '45', 'label_y': '137', 'level': 2, 'chnged': 'N'},
             "09": {'name': 'Matt',     'lamp_x':  '70', 'lamp_y': '147', 'label_x': '105', 'label_y': '137', 'level': 2, 'chnged': 'N'},
             "05": {'name': 'Bench',    'lamp_x': '130', 'lamp_y': '147', 'label_x': '165', 'label_y': '137', 'level': 2, 'chnged': 'N'},
             "06": {'name': 'Kitchen',  'lamp_x': '190', 'lamp_y': '147', 'label_x': '225', 'label_y': '137', 'level': 2, 'chnged': 'N'},
             "0D": {'name': 'Family',   'lamp_x':  '10', 'lamp_y':  '83', 'label_x':  '45', 'label_y':  '73', 'level': 2, 'chnged': 'N'},
             "03": {'name': 'Alex',     'lamp_x':  '70', 'lamp_y':  '83', 'label_x': '105', 'label_y':  '73', 'level': 2, 'chnged': 'N'},
             "0B": {'name': 'Laundry',  'lamp_x': '130', 'lamp_y':  '83', 'label_x': '165', 'label_y':  '73', 'level': 2, 'chnged': 'N'},
             "08": {'name': 'Side',     'lamp_x': '190', 'lamp_y':  '83', 'label_x': '225', 'label_y':  '73', 'level': 2, 'chnged': 'N'},
             "01": {'name': 'Deck',     'lamp_x':  '10', 'lamp_y':  '19', 'label_x':  '45', 'label_y':   '9', 'level': 2, 'chnged': 'N'},
             "00": {'name': 'Hall',     'lamp_x':  '70', 'lamp_y':  '19', 'label_x': '105', 'label_y':   '9', 'level': 2, 'chnged': 'N'},
             "02": {'name': 'B/Room',   'lamp_x': '130', 'lamp_y':  '19', 'label_x': '165', 'label_y':   '9', 'level': 2, 'chnged': 'N'},
             "07": {'name': 'Alex2',    'lamp_x': '190', 'lamp_y':  '19', 'label_x': '225', 'label_y':   '9', 'level': 2, 'chnged': 'N'}
             }


# cbus parameters
cbusinit = ['~~~\n\r','A3210038g\n\r','A3420002g\n\r','A33000777g\n\r']
group = ["16", "14", "0A", "15", "12", "13", "11", "10", "09", "0C", "06", "05", "0B", "08", "0D", "01", "03", "00",
         "02", "07", "FF"]
location = ["Porch", "Entrance", "Passage", "Study", "Master", "Lounge", "Bathroom", "Toilet", "Matt", "Dining",
            "Kitchen", "Bench", "Laundry", "Side", "Family", "Deck", "Alex", "Vestibule", "Ensuite", "Alex2", "All"]

validhex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','\n','\r']

cbus = ''
ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port
update = False

lightq = queue.Queue(maxsize=20)
lightpload = ()
cbusjson = {}

clientid = hex(uuid.getnode())

lastsent = time.time()

cbustest = 'D838006668AA0AA6260000000000000000000000000000000016'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("CBUS/LIGHT")

def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")
    pass

# The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))
#     parsed_cbus = json.loads(str(msg.payload.decode("utf-8")))
#     if int(parsed_cbus['Level']) > 0:
#         LampStatus.drawlamp(gridlines, 'On', int(cbuslamps[parsed_cbus['Group']]['lamp_x']),
#                             int(cbuslamps[parsed_cbus['Group']]['lamp_y']))
#     else:
#         LampStatus.drawlamp(gridlines, 'Off', int(cbuslamps[parsed_cbus['Group']]['lamp_x']),
#                             int(cbuslamps[parsed_cbus['Group']]['lamp_y']))
#     LampStatus.refreshscreen()


def decodeMMI(lightstatus):
    lampgroup = 0
    lamploc = ''
    update = False
    for x in range(0,12,2):
        lamps = lightstatus[x:x+2]
        light = int(lamps,16)
        for y in range(4):
            state = light % 4
            ww = '{0:02x}'.format(lampgroup).upper()
            if  ww in group:
                zz = group.index(ww)
                lamploc = location[zz]
            if state == 1:
#                print('{} {} is On {} {}'.format(ww, lamploc,state, cbuslamps[ww]['level']))
                if state != cbuslamps[ww]['level']:
                    cbuslamps[ww]['level'] = state
                    LampStatus.drawlamp(gridlines, 'On', int(cbuslamps[ww]['lamp_x']),
                                        int(cbuslamps[ww]['lamp_y']))
                    cbusjson["Action"] = "Switch"
                    cbusjson["Level"] = "50"
                    cbusjson["Group"] = ww
#                    print(json.dumps(cbusjson))
#                    client.publish("cbus/light", json.dumps(cbusjson))
                    publish.single("cbus/light", payload=json.dumps(cbusjson), qos=0, retain=False, hostname="192.168.1.180",
                                   port=1883, client_id= clientid, keepalive=60, will=None, auth=None, tls=None,
                                   protocol=mqtt.MQTTv311, transport="tcp")
#                     lightpload = ("cbus/light", json.dumps(cbusjson), qos=0)
#                     lightq.put(lightpload)
#                     print("Queue Size now {}".format(lightq.qsize()))
                    update = True
#                    print('Changed')
            if state == 2:
#                print('{} {} is Off {} {}'.format(ww, lamploc,state, cbuslamps[ww]['level']))
                if state != cbuslamps[ww]['level']:
                    cbuslamps[ww]['level'] = state
                    LampStatus.drawlamp(gridlines, 'Off', int(cbuslamps[ww]['lamp_x']),
                                        int(cbuslamps[ww]['lamp_y']))
                    cbusjson["Action"] = "Switch"
                    cbusjson["Level"] = "00"
                    cbusjson["Group"] = ww
#                    print(json.dumps(cbusjson))
#                     client.publish("cbus/light", json.dumps(cbusjson), qos=0)
                    publish.single("cbus/light", payload=json.dumps(cbusjson), qos=0, retain=False,
                                  hostname="192.168.1.180",
                                  port=1883, client_id=clientid, keepalive=60, will=None, auth=None, tls=None,
                                  protocol=mqtt.MQTTv311, transport="tcp")
                    # lightpload = ("cbus/light", json.dumps(cbusjson))
                    # lightq.put(lightpload)
                    # print("Queue Size now {}".format(lightq.qsize()))
                    update = True
#                    print('Changed')
            light = light // 4
            lampgroup += 1
    if update:
        LampStatus.refreshscreen()
        update = False


def PCI_init():
    for z in range (0,4):
        cbinitialise = cbusinit[z]
        ser.write(str.encode(cbinitialise))

lcdback = (0,0,127)
gridlines = (191,191,0)

client = mqtt.Client(client_id=hex(uuid.getnode()), clean_session=True,)
# client.on_connect = on_connect
# client.on_publish = on_publish


# client.on_message = on_message

# client.connect("192.168.1.180", 1883, 60)


# localDisplay.initDisp()
# #localDisplay.labelgrid('Porch', (320, 50), 90, (191,191,0))
# #localDisplay.drawgrid()
# place = (47,275)
# localDisplay.placeonscreen('Porch',place)
pane = 'lightstatus'
LampStatus = TouchScreen.Displaymgr(pane)

LampStatus.clearscreen(lcdback)
LampStatus.refreshscreen()

#z = input('Draw Grid')

LampStatus.drawgrid(gridlines)
LampStatus.refreshscreen()

# lamp = 'Off'
# while True:
#     if lamp == 'Off':
#         lamp = 'On'
#     else:
#         lamp = 'Off'
#     LampStatus.drawlamp(gridlines, lamp,70,275)
#     LampStatus.refreshscreen()
#     z = input('Change Lamp')
lamp = 'Off'
for lamp_id, lamp_info in cbuslamps.items():
    # print(lamp_id)
    # print(int(cbuslamps[lamp_id]['lamp_x']))
    LampStatus.drawlamp(gridlines, lamp, int(cbuslamps[lamp_id]['lamp_x']), int(cbuslamps[lamp_id]['lamp_y']))
LampStatus.refreshscreen()

#zz = input('Now do labels')
for lamp_id, lamp_info in cbuslamps.items():
    # print(lamp_id)
    position = (int(cbuslamps[lamp_id]['label_x']),int(cbuslamps[lamp_id]['label_y']))
    #print(position)
    LampStatus.draw_rotated_text(cbuslamps[lamp_id]['name'], position,90,fill=gridlines)
LampStatus.refreshscreen()


PCI_init()
print("Welcome")

decodeMMI(cbustest[6:18])
#zz = input('New Lamps')
cbustest = 'D838006A68AA0AA62A0000000000000000000000000000000016'
decodeMMI(cbustest[6:18])



while True:
    # if lightq.empty() == False:
    #     if time.time() - lastsent > .5:
    #         print(lightq.qsize())
    #         payload = lightq.get()
    #         print(payload)
    #         lastsent = time.time()
    #         print(client.publish(payload[0], payload[1], qos=0))

    while ser.in_waiting:
        try:
            cbusin = ser.read(1).decode("utf8")
        except UnicodeError:
            continue
        if cbusin not in validhex:
            continue
        if cbusin == '\n':
            if cbus[0:6]  == 'D83800':
                # print(cbus)
                decodeMMI(cbus[6:18])
            cbus = ''
        else:
            if cbusin != '\r':
                cbus = cbus + cbusin
