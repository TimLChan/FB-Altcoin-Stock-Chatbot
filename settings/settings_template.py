#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Chatbot - Settings
    ~~~~~~
    Settings File.

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2020 by Tim Chan'
__version__ = '2.0'
__license__ = 'MIT'

#Get your free API key from https://www.alphavantage.co/support/#api-key
alphavantageapi = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={}&apikey={}'
alphavantagekey = ''

#Get your 2captcha.com API key from inside the Portal
twocaptchakey = ''
twocaptchaapi = 'http://2captcha.com/res.php?key={}&action=getbalance'

#Australian Exchange pricings for BTC. No longer used
indepreserveapi = 'https://api.independentreserve.com/Public/GetMarketSummary?primaryCurrencyCode=xbt&secondaryCurrencyCode=aud'
acxapi = 'https://acx.io/api/v2/tickers/btcaud.json'

#Get your free API key from https://pro.coinmarketcap.com/ - Note, the Free API only allows ONE currency converstion. For this bot, it has been set to USD
cmcapi = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id={}'
cmctokens = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'
cmcapikey = ''

#Enter your Facebook username (normally email) and password here
#OPTIONAL: Specify a useragent
username = ""
password = ''
useragent = ''

adminfbids = [''] #array of Facebook IDs

alertids = {
}

alertcooldown = 3600
