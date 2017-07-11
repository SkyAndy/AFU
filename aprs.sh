#!/bin/bash
# 11/07/2017 SkyAndy aka DO7EN
LAT=5236.63N
LONG=01311.95E
APRS_CALL=DO0SE-B
APRS_PASS=00000
APRS_SERVER=hun.aprs2.net
APRS_PORT=14580
SYMBOL=r
ALT=000114 #feet
OBJ_NAME="DO0SE DMR" # MUST be 9 character long
TIMESTAMP=`date -u +%d%H%M`z
COMMENT="439.975 -9.4Mhz tune it and call CQ http://do0se.datenport.net"
OBJECT=";${OBJ_NAME}*${TIMESTAMP}${LAT}/${LONG}${SYMBOL}/A=${ALT}${COMMENT}"
BTEXT="$APRS_CALL>APN001:${OBJECT}"
LOGIN="User $APRS_CALL pass $APRS_PASS"
# nc or ncat binary
if [ -f /usr/bin/ncat ] ; then
    NC=/usr/bin/ncat
else
    NC=$BIN/ncat
fi
echo -e "${LOGIN}\n${BTEXT}" | $NC -w 10 ${APRS_SERVER} ${APRS_PORT} &>/dev/null


