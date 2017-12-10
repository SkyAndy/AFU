#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
# 03/2017 do7en@darc.de
# Simple Bot to reply to Telegram messages by DO7EN
# This program is dedicated to the public domain under the CC0 license.
# screen -dm -S tgbot /usr/bin/python tgbot_mmdvm_server.py
"""
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import netifaces as ni, subprocess, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import Adafruit_DHT
from ds18b20 import callsensor

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

#hole von eth0 und wlan0 die IP Adresse und egbe diese als Wert zurück
def get_ip(interface):
  try:
    #ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[2][0]['addr']
  except:
    ip = "0.0.0.0"
    pass
  return ip

#holt sich als float 00.00 die Cpu Temperatur und gibt diesen Wert als float zurück
def getCpuTemperatur():
    tempFile = open( "/sys/class/thermal/thermal_zone0/temp" )
    cpu_temp = tempFile.read()
    tempFile.close()
    newer_method_string = "{:.1f}".format(float(cpu_temp)/1000)
    # return float(cpu_temp)/1000
    return newer_method_string

def start(bot, update):
    cmd(bot, update)
    update.message.reply_text('Meine IP ist %s' % (get_ip("eth0")))
    result = os.system("/root/tgbot_mmdvm_client.sh exip")
    klima(bot, update)

def help(bot, update):
    cmd(bot, update)
    update.message.reply_text('Du bist der Admin... /start wie soll ich Dir da helfen ?')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/DS18B20Scircuit2.png', 'rb'))

def vnstati(bot, update):
    update.message.reply_text("eht0 Netzwerkauslastung")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/vnstati/hourly.png', 'rb'))
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/vnstati/summary.png', 'rb'))
    cmd(bot, update)

def top10(bot, update):
    result = os.system("/root/tgbot_mmdvm_client.sh top10NET")
    result = os.system("/root/tgbot_mmdvm_client.sh top10RF")
    cmd(bot, update)

def cputemp(bot, update):
    s = getCpuTemperatur()
    update.message.reply_text('%s %sC' % ("Die Aktuelle CPU Temperatur beträgt", s))
    cmd(bot, update)

def klima(bot, update):
    s = getCpuTemperatur()
    update.message.reply_text('%s %sC' % ("CPU Temperatur ", s))
    sensor = Adafruit_DHT.DHT11
    gpio = 17
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    update.message.reply_text('Sensor DHT11: {0:0.1f}°C {1:0.1f}%'.format(temperature,humidity))  
    #Sensoren DS18B20
    sensorcount = 3
    sensors = [['28-0416a19685ff','TRX-DMR-TX'], ['28-0416a15adfff','TRX-DMR-RX'], ['28-0516a19554ff','TRX-EL']];
    for i in range(0, sensorcount):
        s = sensors[i][0]
        update.message.reply_text('Sensor ' + str(sensors[i][1]) + ': ' + str(callsensor(s)) + '°C')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/do0seTemperaturen-Stunde.png', 'rb'))
    cmd(bot, update)

def cmd(bot, update):
    update.message.reply_text("/start /klima /cputemp /top10 /vnstati /trx /help")

def CQ(bot, update):
    update.message.reply_text("boaa halt die Klappe...auto-switch to XLX")

def reboot(bot, update):
    result = os.system("reboot")

def echo(bot, update):
    update.message.reply_text('Hä ? /start "%s"' % (update.message.text))
    cmd(bot, update)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("xxxxxxxxx:xxxxxxxxxx_xxxxxxxxxxxxxxxxxxxx")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cputemp", cputemp))
    dp.add_handler(CommandHandler("klima", klima))
    dp.add_handler(CommandHandler("top10", top10))
    dp.add_handler(CommandHandler("vnstati", vnstati))
    dp.add_handler(CommandHandler("reboot", reboot))
    dp.add_handler(CommandHandler("CQ6EDKOTZ", CQ))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
