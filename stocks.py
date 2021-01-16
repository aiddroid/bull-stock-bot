#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple stock api.

"""

import requests

from config import FINNHUB_TOKEN

def get_stock_code(stock_name):
    """Get stock code by name"""
    if stock_name == '拼多多':
        return 'PDD'
    elif stock_name == '百度':
        return 'BIDU'

    return None


def get_stock_info(stock_code):
    """Get stock info by code"""
    r = requests.get('https://finnhub.io/api/v1/quote?symbol={}&token={}'.format(stock_code, FINNHUB_TOKEN))
    if r.status_code == 200:
        info = r.json()
        # current price should greater than 0
        if info['c'] > 0:
            return info
    
    return None
