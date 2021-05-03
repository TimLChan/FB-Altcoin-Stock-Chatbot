#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Chatbot - Stocks Plugin
    ~~~~~~
    Return Stock information from AlphaVantage

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2020 by Tim Chan'
__version__ = '2.0'
__license__ = 'MIT'


import json
import requests
import settings.settings as config
import plugins.common as helper

class Stocks(object):

    def __init__(self):
        self.stockrequests = requests.Session()
        helper.logmessage('Loaded Stocks plugin')

    def parse_stockcode(self, message):
        messagecontent = helper.parsemessage(message)
        if messagecontent and messagecontent.translate(str.maketrans('', '', '!-:.^')).isalnum():
            return messagecontent.upper()[:15]

    def check_stock(self, message):
        stockcode = self.parse_stockcode(message)
        url = config.alphavantageapi.format(stockcode, config.alphavantagekey)
        response = self.stockrequests.get(url)
        stockchart = response.json()

        if 'Global Quote' not in stockchart:
            respstring =  'Nothing found for ' + stockcode
        
        else:
            stockres = stockchart['Global Quote']
            if len(stockres) > 0:
                currprice = '{0:.2f}'.format(float(stockres['05. price']))
                respstring = '{} Price: ${} | Change: ${} ({})'.format(stockres['01. symbol'], currprice, helper.float_to_str(float(stockres['09. change']),2), stockres['10. change percent'])
            else:
                respstring =  'Nothing found for ' + stockcode

        return respstring

