#!/usr/bin/env python

 #####################################################################
#                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#                    Version 2, December 2004                         #
#                                                                     #
# Copyright (C) 2012 Thomas Bertani <mail@thomasbertani.it>           #
#                                                                     #
# Everyone is permitted to copy and distribute verbatim or modified   #
# copies of this license document, and changing it is allowed as long #
# as the name is changed.                                             #
#                                                                     #
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE              #
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION   #
#                                                                     #
#  0. You just DO WHAT THE FUCK YOU WANT TO.                          #
#                                                                     #
 #####################################################################
#                                                                     #
#     Just a test for the force-feedback vibration motor of           #
#     some gamepads.                                                  #
#                                                                     #
 #####################################################################

import usb
from time import sleep

def update(i, js, value):
    value = int(value, 16)
    if (i.idVendor == 0x79 and i.idProduct == 0x6): #DragonRise Inc. Generic USB Joystick
        for i in range(2*3):
             js.interruptWrite(0x01, (0xfa, 0xfe, 0, 0, 0, 0, 0, 0) if not i%2 else (0x51, 0, 0, 0, value, 0, 0, 0))
             js.interruptWrite(0x81, "")
        return
    elif (i.idVendor == 0x7b5 and i.idProduct == 0x312): #Mega World International, Ltd Gamepad
        js.controlMsg(0x21, 9, (0x02, 0, value, value, value))
        return

d = None

for b in usb.busses():
    for i in b.devices:
        if (i.idVendor == 0x79 and i.idProduct == 0x6) or (i.idVendor == 0x7b5 and i.idProduct == 0x312): d = i

if d is None: exit("Device not found")

js = d.open()
try: js.detachKernelDriver(0)
except: pass

js.setConfiguration(1)
js.claimInterface(0)
while True:
    try: update(d, js, raw_input("[0x00-0xff] "))
    except EOFError: break
    except: print "[!] fail"

js.releaseInterface()
