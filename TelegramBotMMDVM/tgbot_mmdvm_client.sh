#!/bin/bash
# Logfiles liegen in der RAMDisk vom MMDVM
KEY="xxxxxxxxx:xxxxxxxxxxxxx_xxxxxxxxxxxxxxxxxxxxx"
# curl https://api.telegram.org/bot$KEY/getUpdates bekommt man die ChatId
bot_chatid="xxxxxxxxx"
bot_chat_text=`uptime`

eth0_IP=`ifconfig eth0 | grep "inet Adress" | cut -d":" -f2 | cut -d" " -f 1`
ex_IP=$(dig -4 @resolver1.opendns.com -t a myip.opendns.com +short)
top10net=$(grep "received network voice header" /mnt/RAMDisk/*.log | cut -d " " -f15,12,14| sort -n | uniq -c | sort -n | tac | head -n 15| sed -e "s/\     //g" | sed -e "s/\ / \t/g")
date=`date +%Y-%m-%d`
top10day=$(grep "received network voice header" /mnt/RAMDisk/MMDVM-$date.log | cut -d " " -f15,12,14| sort -n | uniq -c | sort -n | tac | head -n 15| sed -e "s/\     //g" | sed -e "s/\ / \t/g")
top10rf=$(grep "received RF voice header" /mnt/RAMDisk/*.log | cut -d " " -f15,12,14| sort -n | uniq -c | sort -n|tac | head -n 15 | sed -e "s/\     //g" | sed -e "s/\ / \t/g")
top10xlx=$(grep "received network voice header from" /mnt/RAMDisk/MMDVM-$date.log | grep "TG 270" | cut -d" " -f 12 | sort -n | uniq -c | sort -n | tac | head -15 | sed -e "s/\     //g" | sed -e "s/\ / \t/g")
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

case "$1" in
    exip)
        sendetext "http://$ex_IP:8014/MMDV/"
        sendetext "http://$ex_IP:8014/vnstati/"
        ;;
    top10NET)
        sendetext "Aus dem Netz->HF"
        sendetext "$top10net"
        sendetext "Top 10 von Heute Net->HF"
        sendetext "$top10day"
        sendetext "Top XLX"
        sendetext "$top10xlx"
        ;;
    top10RF)
        sendetext "Direkt gehörte Stationen"
        sendetext "$top10rf"
        ;;
    eth0ip)
        sendetext $eth0_IP
        ;;
    kernel)
        kernelv=`uname -a`
        sendetext $kernelv
        ;;
    sabbeln)
        sendtext "$1"
        ;;
    *)
esac
