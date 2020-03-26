#!/usr/bin/env python3

import os
import sys
import simpleaudio as sa
import wiringpi
import wpi

BTTN1 = 15          # Physical Pin #8
BTTN2 = 16          # Physical Pin #10
BTTN3 = 1           # Physical Pin #12
BTTN4 = 4           # Physical Pin #16
BTTN5 = 5           # Physical Pin #18
BTTN6 = 6           # Physical Pin #22
BTTN7 = 10          # Physical Pin #24
BTTN8 = 11          # Physical Pin #26

BTTN1_LIGHT = 21    # Physical Pin #29
BTTN2_LIGHT = 22    # Physical Pin #31
BTTN3_LIGHT = 23    # Physical Pin #33
BTTN4_LIGHT = 24    # Physical Pin #35
BTTN5_LIGHT = 25    # Physical Pin #37
BTTN6_LIGHT = 27    # Physical Pin #36
BTTN7_LIGHT = 28    # Physical Pin #38
BTTN8_LIGHT = 29    # Physical Pin #40

TEST = 7

# *********
# TODO: Find the sounds we acutally want to use for this project
# Probably want to load them from disk from a folder?
# *********
# Load all sounds
bttnSounds = []
bttnSounds.append(sa.WaveObject.from_wave_file("alert1.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert2.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert3.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert4.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert5.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert1.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert1.wav"))
bttnSounds.append(sa.WaveObject.from_wave_file("alert1.wav"))


# ISR Callbacks (No software debounce because an RC circuit is doing a hardware debounce)
def bttn_1_changed():
    handle_pin_change(BTTN1, 1)
def bttn_2_changed():
    handle_pin_change(BTTN2, 2)
def bttn_3_changed():
    handle_pin_change(BTTN3, 3)
def bttn_4_changed():
    handle_pin_change(BTTN4, 4)
def bttn_5_changed():
    handle_pin_change(BTTN5, 5)
def bttn_6_changed():
    handle_pin_change(BTTN6, 6)
def bttn_7_changed():
    handle_pin_change(BTTN7, 7)
def bttn_8_changed():
    handle_pin_change(BTTN8, 8)

def handle_pin_change(bttnPin,bttnIndex):
    # ***************
    wiringpi.delay(25)   #TODO: REMOVE - Once the circuit board is built, it will do hardware debouncing
    # ***************

    # Read Input
    value = wiringpi.digitalRead(bttnPin)
    print("BTTN{0} = {1}".format(bttnIndex, value))
    if value == wpi.HIGH:
        bttnSounds[bttnIndex].play()
    else:
    
    # Set lighting to match the button
    wiringpi.digitalWrite(bttnPin, value)


# Configure wiringpi
wiringpi.wiringPiSetup()    # This uses the wiringPi number scheme (If you don't know the numbering, just do a `gpio readall` in the cmdline for info)

# Configure all the INPUTS
wiringpi.pinMode(BTTN1, wpi.INPUT)
wiringpi.pinMode(BTTN2, wpi.INPUT)
wiringpi.pinMode(BTTN3, wpi.INPUT)
wiringpi.pinMode(BTTN4, wpi.INPUT)
wiringpi.pinMode(BTTN5, wpi.INPUT)
wiringpi.pinMode(BTTN6, wpi.INPUT)
wiringpi.pinMode(BTTN7, wpi.INPUT)
wiringpi.pinMode(BTTN8, wpi.INPUT)
wiringpi.pullUpDnControl(BTTN1, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN2, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN3, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN4, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN5, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN6, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN7, wpi.PUD_DOWN)
wiringpi.pullUpDnControl(BTTN8, wpi.PUD_DOWN)

# Configure all the Lighting OUTPUTS
wiringpi.pinMode(BTTN1_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN2_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN3_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN4_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN5_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN6_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN7_LIGHT, wpi.OUTPUT)
wiringpi.pinMode(BTTN8_LIGHT, wpi.OUTPUT)
wiringpi.digitalWrite(BTTN1_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN2_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN3_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN4_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN5_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN6_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN7_LIGHT, wpi.LOW)
wiringpi.digitalWrite(BTTN8_LIGHT, wpi.LOW)

# ***************
wiringpi.pinMode(TEST, wpi.OUTPUT)      #TODO: REMOVE - This is here so I can touch wires together to test the inputs.
# ***************

# Configure All ISRs for button press notification
wiringpi.wiringPiISR(BTTN2, wpi.INT_EDGE_BOTH, bttn_2_changed)
wiringpi.wiringPiISR(BTTN1, wpi.INT_EDGE_BOTH, bttn_1_changed)
wiringpi.wiringPiISR(BTTN3, wpi.INT_EDGE_BOTH, bttn_3_changed)
wiringpi.wiringPiISR(BTTN4, wpi.INT_EDGE_BOTH, bttn_4_changed)
wiringpi.wiringPiISR(BTTN5, wpi.INT_EDGE_BOTH, bttn_5_changed)
wiringpi.wiringPiISR(BTTN6, wpi.INT_EDGE_BOTH, bttn_6_changed)
wiringpi.wiringPiISR(BTTN7, wpi.INT_EDGE_BOTH, bttn_7_changed)
wiringpi.wiringPiISR(BTTN8, wpi.INT_EDGE_BOTH, bttn_8_changed)

#TODO: Game Logic/Selection. Below is just a way to stall the main thread from exiting
while True:
    wiringpi.delay(2000)
