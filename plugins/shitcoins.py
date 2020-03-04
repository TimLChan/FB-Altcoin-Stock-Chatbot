#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Chatbot - Shitcoin Plugin
    ~~~~~~
    Return Shitcoin information from CMC + some Aussie Exchanges

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2020 by Tim Chan'
__version__ = '1.5'
__license__ = 'MIT'


import json
import requests
import settings.settings as config
import plugins.common as helper



class Shitcoin(object):
    cmcarray = ''

    def __init__(self):
        self.shitcoinrequests = requests.Session()
        self.cmcarray = self.load_cmc()
        helper.logmessage('Loaded Shitcoin plugin')


    def load_cmc(self):
        dataarray = {}
        response = self.shitcoinrequests.get(config.cmctokens)
        respjson = response.json()
        for obj in respjson:
            dataarray[obj["symbol"]] = obj["id"]
        helper.logmessage('Loaded CoinMarketCap tokens')
        return dataarray

    def get_cmcaltcoin(self, token):
        helper.logmessage('Shitcoin Triggered')
        try:
            response = self.shitcoinrequests.get(config.cmcapi.format(str(self.cmcarray[token.upper()])))
            cmcres = response.json()
            respstring = 'Current {} price: {} USD ({}% change) | {} BTC'.format(cmcres["data"]["website_slug"].capitalize(), helper.float_to_str(cmcres["data"]["quotes"]["USD"]["price"], 10), cmcres["data"]["quotes"]["USD"]["percent_change_24h"], helper.float_to_str(cmcres["data"]["quotes"]["BTC"]["price"], 8))
        except:
            respstring = ('Nothing found for ' + token)
        return respstring
            

