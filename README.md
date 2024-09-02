# NanoAWOS
Nano Automated Weather Observing System is a small platform based on NanoPI NEO v1.4 designed to be connected with YAESU FT550 (or similar) to transfer over the air AWOS information triggered by radio button clicks (PTT clicks).

# Vision
The idea of NanoAWOS is to be assabled with minimal knowledge into electronics and soldering, by utilising a ready NanoPI Neo complete starter kit  by FriendlyELEC (https://www.friendlyelec.com/index.php?route=product/product&product_id=190) 
and be either stand-alone or connected to Home Assistant where flightradar/flightaware with dump1090 and rtl433 can be used to create automation use-cases in small CTAF/non-towered/ATZ areas. 
NanoAWOS is utilising the sound card microphone and that can be used for future voice-to-test->AI use-cases. 

# Features
- Read wundergrund station wind with 4 click (stand-alone)
- Read wundergrund station weather(wind, temp, qnh, density altitude etc) with 6 clicks (stand-alone).
- Stream over the IP network sounds and Text To Speech with Music Player Daemon to the Yaesu 
- Transfer PTT and busy messages over MQTT to Homeassistant
- Create your automation use-cases with home assistant and flight radar on your ATZ area and read:
  - New traffic entered area, read direction with distance
  - New traffic entered pattern
  - Traffic taxi or short/long final 

# Demo
[![YT_VIDEO](https://i9.ytimg.com/vi/fD7kZr5AIl4/mqdefault.jpg?v=66d61968&sqp=CMCy2LYG-oaymwEmCMACELQB8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGGUgXihRMA8=&rs=AOn4CLDl5MSHxLvJRHZshJltsfTD1HXbqA)](https://youtu.be/fD7kZr5AIl4)

# What you need
- NanoPI Neo complete starter kit  by FriendlyELEC (https://www.friendlyelec.com/index.php?route=product/product&product_id=190)
- 1x 4 pin/pole jack 17,5mm to RCA (https://pl.aliexpress.com/item/1005005704133516.html?spm=a2g0o.order_detail.order_detail_item.4.158543cepoLrPJ&gatewayAdapt=glo2pol)
[![jack17](https://github.com/wdcapl/nanoawos/blob/main/img/4pin17jack.png?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/4pin17jack.png?raw=true)
- Panasonic AQY211EH Silicon Relay 
[![relay](https://sigma.octopart.com/cdn-cgi/image/width=75,fit=contain,quality=85,format=auto/23734562/image/Panasonic-AQY211EH.jpg)](https://octopart.com/aqy211eh-panasonic-5821337?gad_source=1&gclid=CjwKCAjwxNW2BhAkEiwA24Cm9A9iLzQBnr-M53DJD7saN16iJo81ng_fFqXxew6HBorU-vJghnyuRxoCYtwQAvD_BwE)

# Assembly

## Add 4 pin support to the NanoHAT board
By using the 17mm jack we are able to extend the standard 3pin stereo jack with 4 pin support. 
- Small spring is needed
- cables
- isolation tape
- glue gun
- basic soldering skills

1. Dissasable the NanoPI kit to get the NanoHat
2. Prepare a small spring (you can buy it in the near store) and cut around 3mm in diameter. 
3. Solder a wire to the spring.
4. Tape/isolate the board and the SMD resistors so when the spring touches them it will not conduct. It is important to use the tape becuse if you mess things up you can easily rip it after glueing and try again.
5. Insert the 17mm jack into the NanoHat and while pushing it in, hold the spring with the wire.
6. Check with a voltometer if all pins work.
7. If all works fine glue the jack socket.
8. Wait 3 min. Check with the voltometer and put the jack in and out to try to see if your new socket works :)
9. This pin should go to the microphone pins of the nanohat
[![speakerpin](https://github.com/wdcapl/nanoawos/blob/main/img/micpin.png?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/micpin.png?raw=true)

It *should* be something like this(it is from one of my many attempts). It should bend more to the right as there is an ethernet port (this is why this attempt did not work ;) )
[![spring](https://github.com/wdcapl/nanoawos/blob/main/img/jack1.JPEG?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/jack1.JPEG?raw=true)

Final result after using the glue gun:
[![gluegun](https://github.com/wdcapl/nanoawos/blob/main/img/jack2.JPEG?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/jack2.JPEG?raw=true)

## Remove one of the stereo channel connections to the main board to use it for PTT
1. There is a pin plastic cover you need to remove
2. Rip the metal connector and put the plastic cover back in.
[![rippin](https://github.com/wdcapl/nanoawos/blob/main/img/PTT_PIn.JPEG?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/PTT_PIn.JPEG?raw=true)
3. The PTT channel should not be connected to the mainboard, we will utilise it for the relay that will be triggered by GPIO
[![pttpin](https://github.com/wdcapl/nanoawos/blob/main/img/ptt_pin.png?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/ptt_pin.png?raw=true)

## Solder the silicon relay to the PTT and GPIO pins. 
1. Use the following schema
[![relayschema](https://github.com/wdcapl/nanoawos/blob/main/img/relayschema.png?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/relayschema.png?raw=true)
2. Please refer to the nanohat schema to confirm all is good (https://wiki.friendlyelec.com/wiki/index.php/NanoPi_NEO#Diagram.2C_Layout_and_Dimension)
3. Final result should be something like this
[![final1](https://github.com/wdcapl/nanoawos/blob/main/img/relay.JPEG?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/relay.JPEG?raw=true)
[![final2](https://github.com/wdcapl/nanoawos/blob/main/img/final.JPEG?raw=true)](https://github.com/wdcapl/nanoawos/blob/main/img/final.JPEG?raw=true)

# Disclaimer
This project is an open-source initiative designed specifically for small aviation purposes. It is important to note that this project has not been certified, endorsed, or approved by any aviation regulatory authorities, including but not limited to the International Civil Aviation Organization (ICAO) or the Federal Aviation Administration (FAA).

Users are responsible for ensuring compliance with all applicable laws, regulations, and safety standards when using this project. This software is provided "as-is," without any express or implied warranties, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. The use of this software is entirely at your own risk.
