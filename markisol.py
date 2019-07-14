#!/usr/bin/python

"""
* Markisol iFit Spring Pro 433.92MHz window shades
* Also sold under the name Feelstyle and various Chinese brands like Bofu
* Compatible with remotes like BF-101, BF-301, BF-305, possibly others
*
* Code by Antti Kirjavainen (antti.kirjavainen [_at_] gmail.com)
*
* This is a Python implementation of the Markisol protocol, for
* the Raspberry Pi. Plug your transmitter to BOARD PIN 16 (BCM/GPIO23).
*
* More info on the protocol in Markisol.ino and RemoteCapture.ino here:
* https://github.com/akirjavainen/markisol
*
* Adapted by: Antoine Mercadal
"""

import time
import sys
import os
import RPi.GPIO as GPIO

USAGE = """
 Usage:
    %s [command]

    commands: 'pair', 'up', 'down', 'stop', 'change', 'limit'.
"""

# Control Commands
SHADE_PAIR = "10111011111011111000001010000011110101001"  # C button
SHADE_DOWN = "10111011111011111000100010000011110110101"  # DOWN button
SHADE_STOP = "10111011111011111000101010000011110110001"  # STOP button
SHADE_UP = "10111011111011111000001110000011110101011"  # UP button
SHADE_LIMIT = "10111011111011111000010010000011110100101"  # L button
SHADE_CHANGE_DIRECTION = "10111011111011111000000110000011110101111"  # STOP + L buttons

TRANSMIT_PIN = 11  # BCM PIN 11 (GPIO17, BOARD PIN 11)
REPEAT_COMMAND = 10


# Microseconds (us) converted to seconds for time.sleep() function:
MARKISOL_AGC1_PULSE = 0.004885
MARKISOL_AGC2_PULSE = 0.00241
MARKISOL_AGC3_PULSE = 0.00132
MARKISOL_RADIO_SILENCE = 0.005045

MARKISOL_PULSE_SHORT = 0.0003
MARKISOL_PULSE_LONG = 0.00068

MARKISOL_COMMAND_BIT_ARRAY_SIZE = 41


def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)


def cleanup():
    # Disable output to transmitter and clean up:
    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
    GPIO.cleanup()


def send(command):
    _sendMarkisolCommand(_convertCmd(command))


def _sendMarkisolCommand(command):

    if len(str(command)) is not MARKISOL_COMMAND_BIT_ARRAY_SIZE:
        print "invalid command:", len(str(command)), "bits long."

    for t in range(REPEAT_COMMAND):
        _doMarkisolTribitSend(command)

    _transmitLow(MARKISOL_RADIO_SILENCE)

    print "> %s" % command.upper()


def _doMarkisolTribitSend(command):

    # AGC bits:
    _transmitHigh(MARKISOL_AGC1_PULSE)  # AGC 1
    _transmitLow(MARKISOL_AGC2_PULSE)  # AGC 2
    _transmitHigh(MARKISOL_AGC3_PULSE)  # AGC 3

    for i in command:

        if i == '0':  # LOW-HIGH-LOW
            _transmitLow(MARKISOL_PULSE_SHORT)
            _transmitHigh(MARKISOL_PULSE_SHORT)
            _transmitLow(MARKISOL_PULSE_SHORT)

        elif i == '1':  # LOW-HIGH-HIGH
            _transmitLow(MARKISOL_PULSE_SHORT)
            _transmitHigh(MARKISOL_PULSE_LONG)

        else:
            print "Invalid character", i, "in command! Exiting..."


def _transmitHigh(delay):
    GPIO.output(TRANSMIT_PIN, GPIO.HIGH)
    time.sleep(delay)


def _transmitLow(delay):
    GPIO.output(TRANSMIT_PIN, GPIO.LOW)
    time.sleep(delay)


def _convertCmd(cmd_string):
    if cmd_string.lower() == "up":
        return SHADE_UP
    elif cmd_string.lower() == "down":
        return SHADE_DOWN
    elif cmd_string.lower() == "stop":
        return SHADE_STOP
    elif cmd_string.lower() == "limit":
        return SHADE_LIMIT
    elif cmd_string.lower() == "change":
        return SHADE_CHANGE_DIRECTION
    elif cmd_string.lower() == "pair":
        return SHADE_PAIR
    else:
        raise Exception("Unknown command '%s'" % cmd_string)


# ------------------------------------------------------------------
# Main program:
# ------------------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "%s" % (USAGE % os.path.basename(sys.argv[0]))
        exit()

    argv_cmd = sys.argv[1]

    init()
    _sendMarkisolCommand(_convertCmd(argv_cmd))
    cleanup()
