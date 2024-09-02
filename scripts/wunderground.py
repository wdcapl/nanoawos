#!/usr/bin/python3 -u
from datetime import date
from pprint import pprint
import subprocess
import math
import json

from wunderground_pws import WUndergroundAPI, units

path = "/usr/local/tts/"

wu = WUndergroundAPI(
    api_key='',
    default_station_id='IGIYN1',
    units=units.METRIC_UNITS,
)
metric=wu.current()['observations'][0]

wu = WUndergroundAPI(
    api_key='',
    default_station_id='IGIYN1',
    units=units.ENGLISH_UNITS,
)
english=wu.current()['observations'][0]

time_hour = list(metric['obsTimeUtc'].split("T")[1].split(':')[i] for i in [0,1])
time_hour = time_hour[0]+time_hour[1]

wind = str(english['winddir'])

windSpeed = str(english['imperial']['windSpeed'])

windGusts = []
if english['imperial']['windGust'] > english['imperial']['windSpeed']:
    windGusts = ['gusts']+[*str(english['imperial']['windGust'])]

print(time_hour)
print(json.dumps(metric,indent=5))
#f = open("/tmp/metar","w")
#f.write("EPMY "+time_hour+" "+wind+" "+windSpeed+windGusts[1]+" "+str(metric['metric']['temp'])+"/"+str(metric['metric']['dewpt'])+" Q"+str(metric['metric']['pressure']))
#f.close()

part1 = [
    'echo',
    'papa',
    'mike',
    'yankee',
    'awos']

part2 = ['zulu',
    'weather',
    'wind'
    ]

part3 = ['at'] + [*windSpeed] + windGusts

part4 = ['temperature'] + [*str(metric['metric']['temp'])] + ['dewpoint'] + [*str(metric['metric']['dewpt'])]

part5 = ['qnh'] + [*str(math.ceil(metric['metric']['pressure']))]

#density alt calc
pressure_alt = 230 + (1013 - metric['metric']['pressure']) * 30
standard_temp = 15 - (2 * (230/1000))
humidity_correction = 0.1 * (metric['metric']['temp'] - metric['metric']['dewpt'])
density_alt = str(math.ceil(pressure_alt + (120 * (metric['metric']['temp'] - standard_temp)) + humidity_correction))
print(str(density_alt))

part6 = ['da'] + [*str(density_alt)] + ['feet']

telegram = part1 + [*time_hour] + part2 + [*wind] + part3 + part4 + part5 + part6

subprocess.run(['mpc','rm','full'])
subprocess.run(['mpc','rm','wind'])

subprocess.run(['mpc','clear'])
for phrase in telegram:
    if phrase == "-":
        subprocess.run(['mpc','add',path+"minus.wav"])
    else:
        subprocess.run(['mpc','add',path+phrase+".wav"])

subprocess.run(['mpc','save','full'])

subprocess.run(['mpc','clear'])
for phrase in ['wind']+[*wind]+part3:
    subprocess.run(['mpc','add',path+phrase+".wav"])

subprocess.run(['mpc','save','wind'])
