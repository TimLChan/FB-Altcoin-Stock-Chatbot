#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Altcoin Stock Chatbot
    ~~~~~~
    Altcoin and Stock chatbot for Python

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2017 by Tim Chan'
__version__ = '1.3'
__license__ = 'MIT'


import fbchat
import json
import random
import decimal
import os
import threading
import urllib3
import re
urllib3.disable_warnings()
from wsgiref.simple_server import make_server, WSGIRequestHandler

#Add html serving to make sure server is always online
def httpserve(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Server is UP']
    
#Get rid of HTTP logs from http://stackoverflow.com/a/31904641
class NoLoggingWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        pass

#Subclass fbchat.Client and override required methods
class AltCoinBot(fbchat.Client):
    httphandler = urllib3.PoolManager()
    urlau = "https://api.independentreserve.com/Public/GetMarketSummary?primaryCurrencyCode=xbt&secondaryCurrencyCode=aud"
    urlacx = "https://acx.io/api/v2/tickers/btcaud.json"
    ctx = decimal.Context()
    
    def __init__(self,email, password, debug=False, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        print('Successfully Loaded')
        
    def float_to_str(self,f,prec):
        """
        Convert the given float to a string,
        without resorting to scientific notation
        """
        """ Thanks to http://stackoverflow.com/posts/38847691/revisions """
        f = float(f) #Casting to float cause Poloniex is a string while others are already floats. And float(float) doesn't break anything... yet
        self.ctx.prec = prec
        d1 = self.ctx.create_decimal(repr(f))
        return format(d1, 'f')
    
    def check_stock(self, stockcode):
        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + stockcode + '%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&format=json'
        response = self.httphandler.request('GET', url)
        stockchart = json.loads(response.data.decode('utf-8'))
        if stockchart['query']['count'] != 0:
            stockres = stockchart['query']['results']['quote']
            if stockres['Ask']:
                return '{} ({}) Price: ${} | Change: ${} ({})'.format(stockres['Name'], stockres['Symbol'], stockres['LastTradePriceOnly'], stockres['Change'], stockres['ChangeinPercent'])   
            else:
                return 'Nothing found for ' + stockcode
        else:
            return 'Nothing found for ' + stockcode
            
    def get_cryptocompare(self, altcoin):
        respstring = 'Current ' + altcoin + ' price: '
        urlbuilder = 'https://min-api.cryptocompare.com/data/price?fsym=' + altcoin + '&tsyms=USD,BTC'
        response = self.httphandler.request('GET', urlbuilder)
        btcchart = json.loads(response.data.decode('utf-8'))
        
        if 'Response' not in btcchart:
            if 'USD' in btcchart:
                respstring += '$' + self.float_to_str(btcchart['USD'],8) + ' USD'
            if 'BTC' in btcchart:
                respstring += ' | ' + self.float_to_str(btcchart['BTC'],8) + ' BTC'
        else:
            respstring = btcchart['Message']
        return respstring
        
    def get_captchacredit(self):
        respstring = 'Current 2Captcha balance: $'
        urlbuilder = 'http://2captcha.com/res.php?key=<YOUR API KEY HERE>&action=getbalance'
        response = self.httphandler.request('GET', urlbuilder)
        respstring += response.data.decode('utf-8')
        return respstring
    
    def get_poloniex(self, altcoin):
        usdtprice = 'USDT_' + altcoin
        btcprice = 'BTC_' + altcoin   
        urlbuilder = 'https://poloniex.com/public?command=returnTicker'  
        response = self.httphandler.request('GET', urlbuilder)
        btcchart = json.loads(response.data.decode('utf-8'))
        if btcprice in btcchart or btcprice == 'BTC_BTC':
            if btcprice == 'BTC_BTC':
                respstring = 'Current {} price (Poloniex): {} USD ({}% change)'.format(altcoin, self.float_to_str(btcchart[usdtprice]['last'],8), self.float_to_str(float(btcchart[usdtprice]['percentChange'])*100,4))
            else:
                if usdtprice in btcchart:
                    respstring = 'Current {} price (Poloniex): {} USD ({}% change) | {} BTC ({}% change)'.format(altcoin, self.float_to_str(btcchart[usdtprice]['last'],8), self.float_to_str(float(btcchart[usdtprice]['percentChange'])*100,4), self.float_to_str(btcchart[btcprice]['last'],8), self.float_to_str(float(btcchart[btcprice]['percentChange'])*100,4))
                else:
                    respstring = 'Current {} price (Poloniex): {} BTC ({}% change)'.format(altcoin, self.float_to_str(btcchart[btcprice]['last'],8), self.float_to_str(float(btcchart[btcprice]['percentChange'])*100,4))
        else:
            respstring = 'Poloniex does not support {} currently'.format(altcoin)
        return respstring
    
    def get_coinbase(self, altcoin):
        if altcoin == 'BTC' or altcoin == 'ETH' or altcoin == 'LTC':
            urlbuilder = 'https://api.coinbase.com/v2/prices/{}-USD/spot'.format(altcoin)
            response = self.httphandler.request('GET', urlbuilder)
            altcoindata = json.loads(response.data.decode('utf-8'))
            respstring = 'Current {} price (Coinbase): {} USD'.format(altcoin, altcoindata['data']['amount'])
            return respstring
        else:
            return 'Coinbase does not support {}'.format(altcoin)
    
    def anti_gyazo(self, url):
        newurl = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
        newurl = newurl.replace("gyazo.com","i.gyazo.com")
        newurl += ".png"
        return newurl
        
    def on_message_new(self, mid, author_id, message, metadata, recipient_id, thread_type):
        self.markAsDelivered(recipient_id, mid) #mark delivered
        self.markAsRead(recipient_id) #mark read
        
        if str(author_id) != str(self.uid):
            chatline = str(message).lower()
            
            if chatline.startswith('!stock'):
                    print('Stock request triggered')
                    messagecontent = chatline.split(' ')
                    if messagecontent[1] and messagecontent[1].translate(str.maketrans('', '', '!-:.')).isalnum():
                        stockcode = messagecontent[1].upper()[:10]
                        respstring = self.check_stock(stockcode)
                        self.send(recipient_id,respstring,message_type=thread_type)
             
            elif chatline.startswith("!decide"):
                decisions = chatline[7:].split(',')
                kinda_random = random.SystemRandom()
                sendstr = 'Decision: {}'.format(kinda_random.choice(decisions).strip())
                self.send(recipient_id,sendstr,message_type=thread_type)
            
            elif chatline.startswith('!nbnpoi'):
                print('NBN POI command triggered')
                response = self.httphandler.request('GET', 'NBN POI CHECKER URL GOES HERE')
                respstring = response.data
                self.send(recipient_id,respstring,message_type=thread_type)
            
            elif chatline.startswith('!math '):
                print('Calculation Triggered')
                messagecontent = chatline[6:]
                if messagecontent.translate(str.maketrans('', '', ' +-*/.^')).isnumeric():
                    messagecontent = messagecontent.replace('^','**')
                    try:
                        respstring = 'Result: ' + self.float_to_str(eval(messagecontent),8)
                    except:
                        respstring = 'Number too big :('
                    self.send(recipient_id,respstring,message_type=thread_type)
                    
            elif chatline.startswith('!btcacx'):
                print('BTC to AUD ACX')
                response = self.httphandler.request('GET', self.urlacx)
                btcchart = json.loads(response.data.decode('utf-8'))
                sendstr = 'Current BTC Price (ACX.IO): A$' + self.float_to_str(btcchart['ticker']['last'],8)
                self.send(recipient_id,sendstr,message_type=thread_type)
            
            elif chatline.startswith('!btcaud'):
                print('BTC to AUD independent')
                response = self.httphandler.request('GET', self.urlau)
                btcchart = json.loads(response.data.decode('utf-8'))
                sendstr = 'Current BTC Price (IndependentReserve): A$' + self.float_to_str(btcchart['LastPrice'],8)
                self.send(recipient_id,sendstr,message_type=thread_type)
                
            elif chatline.startswith('!captcha'):
                print('Randys 2Captcha Called')
                respstring = self.get_captchacredit()
                self.send(recipient_id,respstring,message_type=thread_type)
            
            elif "/gyazo.com/" in chatline:
                print('Crappy Gyazo URL')
                respstring = self.anti_gyazo(chatline)
                self.send(recipient_id,respstring,message_type=thread_type)
                
            elif chatline.startswith('!'):
                messagecontent = chatline[1:]
                msg = messagecontent.split(' ')[0].upper()
                
                if len(msg) > 0:
                    msg = ''.join(e for e in msg if e.isalnum())[:6]

                    if messagecontent.endswith('poloniex'):
                        print(msg + ' command triggered (Poloniex)')
                        respstring = self.get_poloniex(msg)
                    
                    elif messagecontent.endswith('coinbase'):
                        print(msg + ' command triggered (Coinbase)')
                        respstring = self.get_coinbase(msg)
                        
                    else:
                        print(msg + ' command triggered (Cryptocompare Aggregator)')
                        respstring = self.get_cryptocompare(msg)

                    self.send(recipient_id,respstring,message_type=thread_type)
                

           
                
   
#Continually serve HTML to show site is online
httpd = make_server(os.environ['OPENSHIFT_PYTHON_IP'], 8080, httpserve, handler_class=NoLoggingWSGIRequestHandler)
thread = threading.Thread(target = httpd.serve_forever)
thread.start()

#Now actually start the bot
bot = AltCoinBot(os.environ['Email'], os.environ['Password'])
bot.listen()

