#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
import stocks

from config import BOT_TOKEN
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # if message text starts with dollar smybol
    r = re.match(r'^\$(.+)$', update.message.text)
    if not r:
        return False

    m = r.group(1)
    stock_code = None
    if re.match(r'^([a-zA-Z])+$', m):
        # for stock code
        stock_code = m
    else:
        # for stock name
        stock_code = stocks.get_stock_code(m)
 
    if not stock_code:
        update.message.reply_text('未找到相关股票:' + m)
        return False
 
    info = stocks.get_stock_info(stock_code)
    text = build_reply_text(stock_code, info)
    update.message.reply_text(text)


def build_reply_text(stock_code, info):
    """Build reply text"""
    if not info:
        return '未查询到股票信息:' + stock_code
 
    return "${} 股票实时信息\n" \
           "涨跌幅: {}%\n" \
           "当前价: ${}\n" \
           "开盘价: ${}\n" \
           "--------------------\n" \
           "最高价: ${}\n" \
           "最低价: ${}".format(stock_code, round((info['c'] - info['pc']) / info['pc'], 4) * 100, info['c'], info['o'], info['h'], info['l'])


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
