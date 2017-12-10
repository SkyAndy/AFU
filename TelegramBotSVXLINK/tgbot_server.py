#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
# 03/2017 do7en@darc.de Andy
# screen -dm -S tgbot /usr/bin/python /home/svxlink/tgbot_server.py
# call this on /etc/rc.local
"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import netifaces as ni, subprocess, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

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
    tempFile = open( "/sys/devices/platform/sunxi-i2c.0/i2c-0/0-0034/temp1_input" )
    cpu_temp = tempFile.read()
    tempFile.close()
    newer_method_string = "{:.1f}".format(float(cpu_temp)/1000)
    # return float(cpu_temp)/1000
    return newer_method_string

def start(bot, update):
    update.message.reply_text('Hi! /help /trx /cputemp /netlinkan /netlinkaus /DB0EE')
    update.message.reply_text('Meine IP ist %s' % (get_ip("eth0")))
    result = os.system("/home/svxlink/tgbotelenata/tgbot.sh exip")

def trx(bot, update):
    keyboard = [[InlineKeyboardButton("Netlink EIN", callback_data='netlinkan'),
                 InlineKeyboardButton("Netlink AUS", callback_data='netlinkaus')],
                 [InlineKeyboardButton("TRX-70cm TX", callback_data='trx1tx'),
                InlineKeyboardButton("TRX-70cm RX", callback_data='trx1rx')],
                 [InlineKeyboardButton("TRX-2m TX", callback_data='trx2tx'),
                InlineKeyboardButton("TRX-2m RX", callback_data='trx2rx')],
                [InlineKeyboardButton("Verbinde zu DB0EE", callback_data='db0ee')],
                [InlineKeyboardButton("ZVEI zu Andy" , callback_data='zveiandy')],
                [InlineKeyboardButton("SvxLink neu starten", callback_data='restart')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('ELENATA TRX:', reply_markup=reply_markup)

def help(bot, update):
    update.message.reply_text('Du bist der Admin... /start wie soll ich Dir da helfen ?')
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/svxlink/tgbotelenata/mini.jpg', 'rb'))

def vnstati(bot, update):
    update.message.reply_text("eht0 Netzwerkauslastung")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/vnstati/hourly.png', 'rb'))
    bot.send_photo(chat_id=update.message.chat_id, photo=open('/var/www/html/vnstati/summary.png', 'rb'))

def cputemp(bot, update):
    s = getCpuTemperatur()
    update.message.reply_text('%s %sC' % ("Die Aktuelle CPU Temperatur beträgt", s))

def zveiandy(bot, update):
    s = "6#0201976##"
    fobj_out = open("/tmp/SimplexLogic","w")
    fobj_out.write("%s" % (s))
    fobj_out.close()

def netlinkan(bot, update):
    s = "*951#"
    fobj_out = open("/tmp/SimplexLogic","w")
    fobj_out.write("%s" % (s))
    fobj_out.close()
    update.message.reply_text("Netlink EIN geschaltet")

def netlinkaus(bot, update):
    s = "*950#"
    fobj_out = open("/tmp/SimplexLogic","w")
    fobj_out.write("%s" % (s))
    fobj_out.close()
    update.message.reply_text("Netlink getrennt")

def eldb0ee(bot, update):
    id = "8#482691#"
    fobj_out = open("/tmp/SimplexLogic","w")
    fobj_out.write("%s" % (id))
    fobj_out.close()
    update.message.reply_text("Verbinde mit DB0EE")
    
def trx1tx(bot, updatee, query):
    result = os.system("/usr/local/bin/gpio -g write 25 1")
    bot.send_message(chat_id=query.message.chat_id, text='TRX-1-TX GPIO 25')
    
def trx1rx(bot, updatee, query):
    result = os.system("/usr/local/bin/gpio -g write 25 0")
    bot.send_message(chat_id=query.message.chat_id, text='TRX-1-RX GPIO 25')

def trx2tx(bot, updatee, query):
    result = os.system("/usr/local/bin/gpio -g write 24 1")
    bot.send_message(chat_id=query.message.chat_id, text='TRX-2-TX GPIO 24')
    
def trx2rx(bot, update, query):
    result = os.system("/usr/local/bin/gpio -g write 24 0")
    bot.send_message(chat_id=query.message.chat_id, text='TRX-2-RX GPIO 24')
    
def echo(bot, update):
    update.message.reply_text(update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def button(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: %s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    x = query.data
    if x == 'netlinkan':
        netlinkan(bot, update)
    elif x == 'netlinkaus':
        netlinkaus(bot, update)
    elif x == 'trx1tx':
        trx1tx(bot, update, query)
    elif x == 'trx1rx':
        trx1rx(bot, update, query)
    elif x == 'trx2tx':
        trx2tx(bot, update, query)
    elif x == 'trx2rx':
        trx2rx(bot, update, query)
    elif x == 'db0ee':
        eldb0ee(bot, update)
    elif x == 'restart':
        bot.send_message(chat_id=query.message.chat_id, text='!!! Starte SvxLink Neu !!!')
        result = os.system("/home/svxlink/startesvxlink.sh")
    elif x == 'zveiandy':
        bot.send_message(chat_id=query.message.chat_id, text='Rufe DO7EN via ZVEI Modul')
        zveiandy(bot, update)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("xxxxxxxxx:xxxxxxxx-xxxxxxxxxxxxxxxxxxxx-xxxxx")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("cputemp", cputemp))
    dp.add_handler(CommandHandler("netlinkan", netlinkan))
    dp.add_handler(CommandHandler("netlinkaus", netlinkaus))
    dp.add_handler(CommandHandler("DB0EE", eldb0ee))
    dp.add_handler(CommandHandler("trx", trx))
    dp.add_handler(CommandHandler("vnstati", vnstati))
    dp.add_handler(CallbackQueryHandler(button))
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
