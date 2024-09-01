# NanoAWOS
Nano Automated Weather Observing System is a small platform based on NanoPI NEO v1.4 designed to be connected with YAESU FT550 (or similar) to transfer over the air AWOS information triggered by radio button clicks (PTT clicks).

# Vision
The idea of NanoAWOS is to be assabled with minimal knowledge into electronics, soldering by utilising a ready NanoPI Neo complete starter kit  by FriendlyELEC (https://www.friendlyelec.com/index.php?route=product/product&product_id=190) 
and be either stand-alone or connected to Home Assistant where flightradar/flightaware with dump1090 and rtl433 can be use to create automation use-cases in small CTAF/non-towered/ATZ areas. 
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


# What you need
- NanoPI Neo complete starter kit  by FriendlyELEC (https://www.friendlyelec.com/index.php?route=product/product&product_id=190) 
