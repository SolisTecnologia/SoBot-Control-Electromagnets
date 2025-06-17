#!/usr/bin/python3
"""
Solis Robot - SoBot

Control_Electromagnets.py: Programming example to control the SoBot by a USB remote control to move and control the electromagnets.

Created By   : Vinicius M. Kawakami and Rodrigo L. de Carvalho
Version      : 2.0

Company: Solis Tecnologia
"""

import inputs
import serial

flag_start = 0
flag_BT_RZ = 0
flag_BT_Z = 0
flag_r5 = 0
flag_r6 = 0
flag_r7 = 0
flag_r8 = 0


# Find the Logitech F710 controller ID connected to the Raspberry Pi
gamepad = inputs.devices.gamepads[0]
print(gamepad)

# Configure the serial port
usb = serial.Serial('/dev/ttyACM0', 57600, timeout=0, dsrdtr=False)
usb.flush()

# Configure wheel parametres
usb.write(b"WP MT1 WD99,84")
usb.write(b"WP MT2 WD99,54")
usb.write(b"WP DW264,95")

# Set the motion proportional gain
usb.write(b"PG SO2,3 CA3,22 DF6,11 RI-6")

# Configure operating parametres in continuous mode
usb.write(b"MT0 MC MD0 AT100 DT100 V8")

while True:
    
    events = inputs.get_gamepad()   # Checks if there was any control event
    
    for event in events:
        
        # Checks if it is event of type "KEY"
        if event.ev_type == "Key":
            print(f"Evento code: {event.code}")
            print(f"Evento state: {event.state}")

            # Check if the event code is "BTN_START" in state 1
            if event.code == "BTN_START" and event.state == 1:
                print("BotÃ£o Start pressionado")
                if flag_start == 0:
                    flag_start = 1
                    usb.write(b"MT0 ME1")               # Enable motors
                    usb.write(b"LT E1 RD0 GR0 BL100")   # Turn on Led Tap

                else:
                    flag_start = 0
                    usb.write(b"MT0 ME0")               # Disable motors
                    usb.write(b"LT E0")                 # Turn off Led Tap

            # Check if the event code is "BTN_SOUTH" in state 1
            if event.code == "BTN_SOUTH" and event.state == 1:
                print("BotÃ£o A pressionado")
                if(flag_r5 == 0):
                    flag_r5 = 1
                    usb.write(b"DO5 E1")
                    print("Rele 5 Ativado")
                else:
                    flag_r5 = 0
                    usb.write(b"DO5 E0")
                    print("Rele 5 Desativado")

            # Check if the event code is "BTN_EAST" in state 1
            elif event.code == "BTN_EAST" and event.state == 1:
                print("BotÃ£o B pressionado")
                print(flag_r6)
                if(flag_r6 == 0):
                    flag_r6 = 1
                    usb.write(b"DO6 E1")
                    print("Rele 6 Ativado")
                else:
                    flag_r6 = 0
                    usb.write(b"DO6 E0")
                    print("Rele 6 Desativado")

            # Check if the event code is "BTN_NORTH" in state 1
            elif event.code == "BTN_NORTH" and event.state == 1:
                print("BotÃ£o X pressionado")
                if(flag_r8 == 0):
                    flag_r8 = 1
                    usb.write(b"DO8 E1")
                    print("Rele 8 Ativado")
                else:
                    flag_r8 = 0
                    usb.write(b"DO8 E0")
                    print("Rele 8 Desativado")

            # Check if the event code is "BTN_WEST" in state 1
            elif event.code == "BTN_WEST" and event.state == 1:
                print("BotÃ£o Y pressionado")
                if(flag_r7 == 0):
                    flag_r7 = 1
                    usb.write(b"DO7 E1")
                    print("Rele 7 Ativado")
                else:
                    flag_r7 = 0
                    usb.write(b"DO7 E0")
                    print("Rele 7 Desativado")

            # Check if the event code is "BTN_TR" in state 1
            elif event.code == "BTN_TR" and event.state == 1:
                print("BotÃ£o RB pressionado")
                # Configure continuous mode with curve on the same axis
                usb.write(b"MT0 MC MD0 AT100 DT100 V8")

            # Check if the event code is "BTN_TL" in state 1
            elif event.code == "BTN_TL" and event.state == 1:
                print("BotÃ£o LB pressionado")
                # Configure continuous mode with differential curve
                usb.write(b"MT0 MC MD1 RI100 AT100 DT100 V8")

        # Checks if it is event of type "Absolute"
        if event.ev_type == "Absolute":
            print(f"Evento code: {event.code}")
            print(f"Evento state: {event.state}")

            ### Buttons to control the direction ###
            # Events with the MODE button disabled
            # Check if the event code is "ABS_HAT0X"
            if event.code == "ABS_HAT0X":
                if flag_start:                  # Check if flag_start is enable
                    if event.state == -1:       # Check state (left direction) of the button
                        print("BotÃ£o ESQ pressionado")
                        usb.write(b"MT0 ML")

                    elif event.state == 1:      # Check state (right direction) of the button
                        print("BotÃ£o DIR pressionado")
                        usb.write(b"MT0 MR")

                    else:
                        usb.write(b"MT0 MP")

            # Check if the event code is "ABS_HAT0Y"
            if event.code == "ABS_HAT0Y":
                if flag_start:                  # Check if flag_start is enable
                    if event.state == -1:       # Check state (front direction) of the button
                        print("BotÃ£o FRENTE pressionado")
                        usb.write(b"MT0 MF")

                    elif event.state == 1:      # Check state (back direction) of the button
                        print("BotÃ£o TRAS pressionado")
                        usb.write(b"MT0 MB")

                    else:
                        usb.write(b"MT0 MP")
            
            ### Buttons to control the lift ###
            # Check if the event code is "ABS_RZ"
            if event.code == "ABS_RZ":
                if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                    if flag_BT_RZ == 0:
                        flag_BT_RZ = 1
                        print("BotÃ£o RZ pressionado")
                        usb.write(b"EL UP")
                elif event.state == 0:
                    print("BotÃ£o RZ solto")
                    flag_BT_RZ = 0
                    usb.write(b"EL ST")

            # Check if the event code is "ABS_Z"
            if event.code == "ABS_Z":
                if event.state >= 1:            # Check if state is greater than 1 (button pressed)
                    if flag_BT_Z == 0:
                        flag_BT_Z = 1
                        print("BotÃ£o Z pressionado")
                        usb.write(b"EL DN")
                elif event.state == 0:
                    print("BotÃ£o Z solto")
                    flag_BT_Z = 0
                    usb.write(b"EL ST")

