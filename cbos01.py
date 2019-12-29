#
# CBus decoder and Display to ILI9341 320 x 240 TFTLCD Display
# 
# Done for Raspberry Pi Zero W as earlier ESP32 version had a habit to stop.
# Once debuggged then maybe return to ESP32 and micropython or circuitpython
#
# Author:  Barry Hay
# Started:  10 Jun 2019
# V0.01  10 June 2019
#
import serial
import localDisplay
import sys


# cbus parameters
cbusinit = ['~~~\n\r','A3210038g\n\r','A3420002g\n\r','A33000777g\n\r']
ramps = ["02", "0A", "12", "1A", "22", "2A", "32", "3A", "42", "4A", "52", "5A", "62", "6A", "72", "7A"]
group = ["16", "14", "0A", "15", "12", "13", "11", "10", "09", "0C", "06", "05", "0B", "08", "0D", "01", "03", "00",
         "02", "07", "FF"]
location = ["Porch", "Entrance", "Passage", "Study", "Master", "Lounge", "Bathroom", "Toilet", "Matt", "Dining",
            "Kitchen", "Bench", "Laundry", "Side", "Family", "Deck", "Alex", "Vestibule", "Ensuite", "Alex2", "All"]


validhex = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','\n','\r']    

cbus = ''
ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port

def PCI_init():
    for z in range (0,4):
        cbinitialise = cbusinit[z]
        ser.write(str.encode(cbinitialise))


def decodeMMI(lightstatus):
    lampgroup = 0
    lamploc = ''
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
                print('{} {} is On'.format(ww, lamploc))
            if state == 2:
                print('{} {} is Off'.format(ww, lamploc))
            light = light // 4
            lampgroup += 1


#localDisplay.initDisp()

PCI_init()
print("Welcome")


while True:
#    c.check_msg()
    while ser.in_waiting:
        #            mqttc.loop()
#        cbusin = uart.read(1)
        try:
            cbusin = ser.read(1).decode("utf8")
#            print(cbusin)
        except UnicodeError:
            continue
        if cbusin not in validhex:
            continue
#        print(cbusin)
        if cbusin == '\n':
#            print(cbus)
            if cbus[0:6]  == 'D83800':
                decodeMMI(cbus[6:18])
                cbus = ''
            else:
                if cbus[6:8] == '01':
                    groupaddr = 12
                    lvl = 14
                    lgtcmd = 10
                else:
                    groupaddr = 10
                    lvl = 12
                    lgtcmd = 8
                if cbus[groupaddr:groupaddr + 2] in group:
                    # cbusjson["Group"] = cbus[groupaddr:groupaddr + 2]
                    yy = group.index(cbus[groupaddr:groupaddr + 2])
                    decodecbus = location[yy]
                    if cbus[lgtcmd:lgtcmd + 2] == '79':
                        decodecbus = decodecbus + "  ON"
                        # cbusjson["Action"] = "Switch"
                        # cbusjson["Level"] = 100
                    elif cbus[lgtcmd:lgtcmd + 2] == '01':
                        decodecbus = decodecbus + "  OFF"
                        # cbusjson["Action"] = "Switch"
                        # cbusjson["Level"] = 0
                    elif cbus[lgtcmd:lgtcmd + 2] in ramps:
                        decodecbus = decodecbus + " Ramp to " + cbus[lvl:lvl + 2]
                        # cbusjson["Action"] = "Ramp"
                        # cbusjson["Level"] = int(int(cbus[lvl:lvl + 2], 16) * 100 / 255)
                    else:
                        decodecbus = cbus
#                    print(decodecbus)
                    #localDisplay.send2screen(decodecbus)
                    # send2oled('-> ' + decodecbus)
                    # print(ujson.dumps(cbusjson))
                    # c.publish(channel, ujson.dumps(cbusjson))
                    #                    mqttc.publish(channel, "dog")
                cbus = ''
        else:
            if cbusin != '\r':
                cbus = cbus + cbusin
#    c.check_msg()
