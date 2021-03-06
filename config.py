#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Bot config.

"""
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "You can create a telegram bot and get bot token from https://t.me/botfather")
FINNHUB_TOKEN = os.getenv("FINNHUB_TOKEN", "You can get finnhub stock api token from https://finnhub.io")

print("BOT_TOKEN: " + BOT_TOKEN)
print("FINNHUB_TOKEN: " + FINNHUB_TOKEN)
