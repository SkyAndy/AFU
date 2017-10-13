#!/bin/bash
# INHALT von /etc/ax25/axports 
# kiss0 DO0SE-1 19200 256 2 438.300 MHz (9600  bps)

# Inhalt von
# [DO0SE-1 via ax0]
# NOCALL * * * * * * L
# default * * * * * * - route /usr/local/sbin/ttylinkd ttylinkd

# evt greift noch etwas auf USB zu.....
/usr/bin/killall -9 kissattach

# DIPSCHALTER TNC2S ^^-------
# Kommunikationsrate Seriel setzten (wie DIPSCHALTER)
stty -F /dev/ttyUSB0 19200
sleep 1

# <ESC>@K senden für den KISS MODUS
echo -en "\r\033@K\r" > /dev/USB0
sleep 2

# Netztwerkarte anlegen
/usr/local/sbin/kissattach -i 10.10.0.5 -m 512 /dev/ttyUSB0 kiss0

# /etc/iproute2/rt_tables
# dort folgende Zeile hinzufügen 
# 1 rt2
# Setzten der ROUTING TABELLE
/sbin/ip route add 10.10.0.0/24 dev ax0 src 10.10.0.10 table rt2
/sbin/ip route add default via 10.10.0.1 dev ax0 table rt2
/sbin/ip rule add from 10.10.0.10/32 table rt2
/sbin/ip rule add to 10.10.0.10/32 table rt2

# Anzeige der routings
/sbin/ip route list table rt2
/sbin/ip rule show
# Anzeige Schnittstelle
ifconfig ax0

# Setze eine Bake ab
beacon -c DO7EN -d WIDE1-1 -s "DO0SE-1" 'PR Test von JO62OO 5W'

# Das ganze kann auch statisch gemacht werden in /etc/network/interfaces
# iface ax0 inet static
#    address 10.10.0.5
#    netmask 255.255.255.0
#    post-up ip route add 10.10.0.0/24 dev eth1 src 10.10.0.10 table rt2
#    post-up ip route add default via 10.10.0.1 dev eth1 table rt2
#    post-up ip rule add from 10.10.0.10/32 table rt2
#    post-up ip rule add to 10.10.0.10/32 table rt2
