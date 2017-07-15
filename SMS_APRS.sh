#!/bin/bash
# 16/07/2017 SkyAndy aka DO7EN
# send SMS via APRS Network
APRS_CALL=DO0SE-B
APRS_PASS=xxxxx
APRS_SERVER=hun.aprs2.net
APRS_PORT=14580
TARGET_CALL="DO7EN    " # MUST be 9 character long
TIMESTAMP=`date -u +%d%H%M`z
SMS="Test to OM via Bash"
OBJECT=":${TARGET_CALL}:${SMS}"
BTEXT="$APRS_CALL>APN001:${OBJECT}"
LOGIN="User $APRS_CALL pass $APRS_PASS"
# nc or ncat binary
if [ -f /usr/bin/ncat ] ; then
    NC=/usr/bin/ncat
else
    NC=$BIN/ncat
fi
echo -e "${LOGIN}\n${BTEXT}" | $NC -w 10 ${APRS_SERVER} ${APRS_PORT} &>/dev/null
