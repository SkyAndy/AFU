#!/bin/bash
# 03/2017 do7en@darc.de Andy
KEY="xxxxxxxxx:xxxxxxxx-xxxxxxxxxxxxxxxxxxxx-xxxxx"
bot_chatid="xxxxxxxxx"
bot_chat_text=`uptime`

eth0_IP=`ifconfig eth0 | grep "inet Adress" | cut -d":" -f2 | cut -d" " -f 1`
ex_IP=$(dig -4 @resolver1.opendns.com -t a myip.opendns.com +short)

# Argumente größer als 0 ?
# xxx.sh aa bb cc ergibt 3 xx.sh aa 'bb 123' cc ergibt auch 3
if [ $# -lt 1 ]; then
    exit 0
fi

function sendetext {
    bot_chat_text=$1
    timeout="10"
    url="https://api.telegram.org/bot$KEY/sendMessage"
    curl -s --max-time $timeout POST -d "chat_id=$bot_chatid&text=$bot_chat_text" $url
}

# aus der TCL heraus:
# suehe Beispiel TCL bei GitHub
# /usr/share/svxlink/events.d/local/SimplexLogic70cm.tcl:  exec /home/svxlink/tgbotelenata/tgbot.sh "Starte $logic_name mit $func"

case "$1" in
    exip)
        sendetext "http://$ex_IP:8013"
        ;;
    eth0ip)
        sendetext $eth0_IP
        ;;
    empfange)
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        sendetext "auf Sendung $DATE"
        ;;
    sende)
        DATE=`date +%Y-%m-%d_%H:%M:%S`
        sendetext "Empfang"
        ;;
    kernel)
        kernelv=`uname -a`
        sendetext $kernelv
        ;;
    *)
        sendetext $"$1"
esac
