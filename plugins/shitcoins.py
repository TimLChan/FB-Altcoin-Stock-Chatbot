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
__version__ = '2.0'
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
            self.headers = {'X-CMC_PRO_API_KEY': config.cmcapikey}
            self.cmcid = str(self.cmcarray[token.upper()])
            response = self.shitcoinrequests.get(config.cmcapi.format(self.cmcid ), headers=self.headers)
            cmcres = response.json()
            respstring = 'Current {} price: {} USD ({}% change)'.format(cmcres["data"][self.cmcid]["name"].capitalize(), helper.float_to_str(cmcres["data"][self.cmcid]["quote"]["USD"]["price"], 10), cmcres["data"][self.cmcid]["quote"]["USD"]["percent_change_24h"])
        except:
            respstring = ('Nothing found for ' + token)
        return respstring
            

