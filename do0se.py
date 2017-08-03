#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# -*- coding: iso-8859-1 -*-
# by DO7EN 30/6/2017
from termcolor import colored
#import RPi.GPIO as GPIO
import os, time, sys, rrdtool
from rrdtool import update as rrd_update
import Adafruit_DHT
#import telegram

# starten mit screen -dm -S rrd /usr/bin/python /home/pi/DO0SE-Temperatur/do0se.py
# screen -rx -S rrd (kann die Seassion und die Ausgaben mit angesehen werden)

# Pfad zum Ordner wo die Bilder gespeichert werden sollen
_html="/var/www/html/"
_rrddatenbank="do0se.rrd"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

sensorpath = '/sys/bus/w1/devices/'
sensorfile = '/w1_slave'

lan = False

#chat_id='xxxxxxxxx'
#bot = telegram.Bot(token='xxx:xxx')

def erstelle():
    ret = rrdtool.create("do0se.rrd", "--step", "200", "--start", '0',
    "DS:dmrrx:GAUGE:2000:U:U",
    "DS:dmrtx:GAUGE:2000:U:U",
    "DS:eltrx:GAUGE:2000:U:U",
    "DS:dht11t:GAUGE:2000:U:U",
    "DS:dht11f:GAUGE:2000:U:U",
    "DS:cpu1:GAUGE:2000:U:U",
    "RRA:AVERAGE:0.5:1:8640",
    "RRA:AVERAGE:0.5:60:1440",
    "RRA:AVERAGE:0.5:60:10080",
    "RRA:AVERAGE:0.5:3600:720",
    "RRA:AVERAGE:0.5:86400:236",
    "RRA:MAX:0.5:1:86400",
    "RRA:MAX:0.5:60:1440",
    "RRA:MAX:0.5:60:10080",
    "RRA:MAX:0.5:3600:720",
    "RRA:MAX:0.5:86400:236")

def update():
    dmrrx = callsensor_ds18b20("28-0416a15adfff")
    dmrtx = callsensor_ds18b20("28-0416a19685ff")
    eltrx = callsensor_ds18b20("28-0516a19554ff")
    
    sensor = Adafruit_DHT.DHT11
    gpio = 17
    dht11f, dht11t = Adafruit_DHT.read_retry(sensor, gpio)
    
    cpu1 = getCpuTemperatur()
    ret = rrd_update('do0se.rrd', 'N:%s:%s:%s:%s:%s:%s' %(dmrrx, dmrtx, eltrx, dht11t, dht11f,cpu1));   
#    luefter(eltrx)

def luefter(temperatur):
    solltemp = 43
    diff = 3
    global lan
    
    if lan == False:
        if temperatur >= (solltemp + diff):
            print colored("sms und einschalten",'red')
            lan = True
            bot.send_message(chat_id=chat_id, text="Elenata TRX hat Hitze %f GPIO:%d" % (temperatur, lan))
    if lan == True:
        if temperatur <= (solltemp - diff):
            print colored("sms und abschalten",'green')
            lan = False
            bot.send_message(chat_id=chat_id, text="Elenata TRX wieder normal %f GPIO:%d" % (temperatur, lan))
    #print colored("Aktuell %f soll:%d diff:%d GPIO:%d" % (temperatur, solltemp, diff, lan),'magenta')
    #bot.send_message(chat_id=chat_id, text="Aktuell %f soll:%d diff:%d GPIO:%d" % (temperatur, solltemp, diff, lan))

def getCpuTemperatur():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    newer_method_string = "{:.1f}".format(float(cpu_temp)/1000)
    # return float(cpu_temp)/1000
    return newer_method_string

def callsensor_ds18b20(sensor):
    try:
        f = open(sensorpath + sensor + sensorfile, 'r')
        lines = f.readlines()
        f.close()
        if lines[0].strip() [-3:] != 'YES':
            sys.exit('Fehler bei Sensor ' + sensor)
        temp_line = lines[1].find('t=')
        if temp_line != -1:
            temp_output = lines[1].strip() [temp_line+2:]
            temp_celsius = float(temp_output) / 1000
    except (IOError), e:
        return str("0")
    return temp_celsius

def messen():
    Messung = 1
    while True:
        time.sleep(10)
        Messung = Messung + 1
        if Messung >= 6:
            Messung = 1
            gfx()
            gfxdht11()
        update()

def gfxdht11():
    for sched in ['Minute' , 'Stunde' , 'Tag' , 'Woche', 'Monat']:
        period = "00"
        if sched == 'Stunde':
            period = 'h'
        elif sched == 'Tag':
            period = 'd'
        elif sched == 'Woche':
            period = 'w'
        elif sched == 'Monat':
            period = 'm'
        ret = rrdtool.graph( "%s/do0seDHT11-%s.png" %(_html, sched), "--start", "-1%s" %(period), "--vertical-label=Ceslsius / Feuchte",
         '--watermark=DO0SE Repeater',
         "-w 800",
         "-h 200",
         "--title=Anzeige der Daten im Zeitraum: %s" %sched,
         "--color=BACK#000000",
         "--color=FONT#FFFFFF",
         "--color=GRID#AAAAAA",
         "--color=MGRID#BBAABB",
         "--color=CANVAS#000000",
         "DEF:dht11t=do0se.rrd:dht11t:AVERAGE",
         "DEF:dht11f=do0se.rrd:dht11f:AVERAGE",
         "VDEF:dht11tAVR=dht11t,AVERAGE",
         "VDEF:dht11fAVR=dht11f,AVERAGE",
         "COMMENT:Messdaten von der Umgebung an DO0SE von %s Uhr\l" %time.strftime("%d.%m.%Y %H.%M"),
         "COMMENT: \l",
         "LINE3:dht11t#228B22: Temperatur",
         "GPRINT:dht11tAVR:%6.2lf %S",
         "LINE3:dht11f#20B2AA: Feuchte",
         "GPRINT:dht11fAVR:%6.2lf %S",
         "HRULE:4#0000FF: Frostschwelle 4C")

def gfx():
    for sched in ['Minute' , 'Stunde' , 'Tag' , 'Woche', 'Monat']:
        period = "00"
        if sched == 'Stunde':
            period = 'h'
        elif sched == 'Tag':
            period = 'd'
        elif sched == 'Woche':
            period = 'w'
        elif sched == 'Monat':
            period = 'm'
        ret = rrdtool.graph( "%s/do0seTemperaturen-%s.png" %(_html, sched), "--start", "-1%s" %(period), "--vertical-label=Celsius",
         '--watermark=DO0SE Repeater',
         "-w 800",
         "-h 200",
         "--title=Anzeige der Temperaturen von den TRX DMR / Echolink im Zeitraum: %s" %sched,
         "--color=BACK#000000",
         "--color=FONT#FFFFFF",
         "--color=GRID#AAAAAA",
         "--color=MGRID#BBAABB",
         "--color=CANVAS#111111",
         "DEF:dmrrx=do0se.rrd:dmrrx:AVERAGE",
         "DEF:dmrtx=do0se.rrd:dmrtx:AVERAGE",
         "DEF:eltrx=do0se.rrd:eltrx:AVERAGE",
         "DEF:cpu1=do0se.rrd:cpu1:AVERAGE",
         "VDEF:dmrtxAVR=dmrtx,AVERAGE",
         "VDEF:dmrrxAVR=dmrrx,AVERAGE",
         "VDEF:eltrxAVR=eltrx,AVERAGE",
         "VDEF:cpu1AVR=cpu1,AVERAGE",
         "COMMENT:Messdaten der Temperaturen am TRX bei DO0SE um %s Uhr\l" %time.strftime("%d.%m.%Y %H.%M"),
         "COMMENT: \l",
         "LINE2:dmrtx#9A2EFE: DMR-TX  ",
         "GPRINT:dmrtxAVR:%6.2lf %S",
         "LINE2:eltrx#00FFFF: ECHOLINK",
         "GPRINT:eltrxAVR:%6.2lf %S\l",
         "LINE2:dmrrx#D0A9F5: DMR-RX  ",
         "GPRINT:dmrrxAVR:%6.2lf %S",
         "LINE1:cpu1#FE2E2E: CPU BGA  ",
         "GPRINT:cpu1AVR:%6.2lf %S\l",
         "HRULE:44#AAAAAA: Ventilator Schaltschwelle bei 44C")

if ( not os.path.isfile(_rrddatenbank)):
    print ("Datenbank %s nicht vorhanden....lege sie neu an" % _rrddatenbank)
    erstelle()

try:
    messen()
except KeyboardInterrupt:
    print('bye....')
    exit()


