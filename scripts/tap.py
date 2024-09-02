#!/usr/bin/python3 -u

# open a microphone in pyAudio and listen for taps

import pyaudio
import struct
import math
import subprocess
from time import sleep
import paho.mqtt.client as mqtt

INITIAL_TAP_THRESHOLD = 0.01
FORMAT = pyaudio.paInt16 
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1
RATE = 44100  
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
# if the noise was longer than this many blocks, it's not a 'tap'
MAX_TAP_BLOCKS = 0.15/INPUT_BLOCK_TIME

def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.tap_threshold = INITIAL_TAP_THRESHOLD
        self.noisycount = MAX_TAP_BLOCKS+1 
        self.quietcount = 0 
        self.errorcount = 0
        self.buttonpress = 0
        self.client = mqtt.Client()
        #self.client.username_pw_set("mqtt", "mqtt-pwd")
        #self.client.connect("192.168.1.64",1883,60)

    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = 3
        for i in range( self.pa.get_device_count() ):     
            devinfo = self.pa.get_device_info_by_index(i)   
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def pressDetected(self):
        print("tap.py: "+str(self.buttonpress) + " tap detected")
        #self.client.publish("yaesu/"+str(self.buttonpress)+"tap", "ON")
        #self.client.publish("yaesu/"+str(self.buttonpress)+"tap", "OFF")
        if self.buttonpress == 6:
            subprocess.run(['mpc','clear'])
            subprocess.run(['mpc','load','full'])
            subprocess.run(['mpc','play'])
        elif self.buttonpress == 4:
            subprocess.run(['mpc','clear'])
            subprocess.run(['mpc','load','wind'])
            subprocess.run(['mpc','play'])

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK,exception_on_overflow = False)
        except IOError as e:
            # dammit. 
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = get_rms( block )
        #print(round(amplitude,3))
        if round(amplitude,2) != self.tap_threshold:
            # noisy block
            #print("NOISY:"+str(round(amplitude,2)))
            self.quietcount = 0
            self.noisycount += 1
#            self.client.publish("yaesu/busy_state", "ON")
        else:            
            # quiet block.
            #print("QUIET:"+str(round(amplitude,3)))
            self.quietcount += 1
            if self.noisycount > 2:
                self.buttonpress += 1
            if self.quietcount == 10:
                self.pressDetected()
                self.buttonpress = 0
            self.noisycount = 0
#self.client.publish("yaesu/busy_state","OFF")
                

if __name__ == "__main__":
    tt = TapTester()

    while True:
        tt.listen()
