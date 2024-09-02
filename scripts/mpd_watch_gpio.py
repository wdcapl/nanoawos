#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

# IMPORTS
import sys
import pprint
import os
from time import sleep

from mpd import (MPDClient, CommandError)
from socket import error as SocketError

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
##
CON_ID = {'host':HOST, 'port':PORT}
##  

## Some functions
def mpdConnect(client, con_id):
    """
    Simple wrapper to connect MPD.
    """
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True

def mpdAuth(client, secret):
    """
    Authenticate
    """
    try:
        client.password(secret)
    except CommandError:
        return False
    return True
##

def main():
    # Check if gpio201 is enabled
    if not os.path.isfile("/sys/class/gpio/gpio201/direction"):
        f = open("/sys/class/gpio/export","w")
        f.write("201")
        f.close()
        f = open("/sys/class/gpio/gpio201/direction","w")
        f.write("out")
        f.close()

    ## MPD object instance
    client = MPDClient()
    if mpdConnect(client, CON_ID):
        print('Got connected!')
    else:
        print('fail to connect MPD server.')
        sys.exit(1)

    playing = 0
    # Auth if password is set non False
    if PASSWORD:
        if mpdAuth(client, PASSWORD):
            print('Pass auth!')
        else:
            print('Error trying to pass auth.')
            client.disconnect()
            sys.exit(2)

    while True:
        if client.status()['state'] == 'play':
            f = open("/sys/class/gpio/gpio201/value","w")
            f.write("1")
            f.close()
            playing = 1
        else:
            if playing == 1:
                f = open("/sys/class/gpio/gpio201/value","w")
                f.write("0")
                f.close()
                playing = 0
        sleep(0.1)

    client.disconnect()
    sys.exit(0)

# Script starts here
if __name__ == "__main__":
    main()
