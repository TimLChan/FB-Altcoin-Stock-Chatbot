#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Altcoin Stock Chatbot
    ~~~~~~
    Altcoin and Stock chatbot for Python

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2020 by Tim Chan'
__version__ = '2.0'
__license__ = 'MIT'


import fbchat
import os
import threading
import requests
from pickle import dump, load
import logging

import settings.settings as config
import plugins.common as helper
import plugins.stocks as Stocks
import plugins.shitcoins as Shitcoins
import plugins.simplereply as Reply
import plugins.misc as Misc


#Subclass fbchat.Client and override required methods
class AltCoinBot(fbchat.Client):
    session_cookies = {}

    def __init__(self, email, password, user_agent=None, logging_level=logging.ERROR):
        self.iphandler = requests.Session()
        response = self.iphandler.get("http://ipv4.icanhazip.com").text
        helper.logmessage('Current IP: ' + response)
        try:
            self.session_cookies = load(open("session_cookie.json", 'rb'))
            helper.logmessage("There is a cookie file!")
            fbchat.Client.__init__(self,email, password, user_agent, max_tries=5, session_cookies=self.session_cookies)
        except:
            # Session Cookie doesn't exist
            helper.logmessage("There is no cookie file!")
            fbchat.Client.__init__(self,email, password, user_agent)


        try:
            self.session_cookies = self.getSession()
            helper.logmessage(self.session_cookies)
            dump(self.session_cookies, open("session_cookie.json", 'wb'))
        except:
            # Session Cookie doesn't exist
            pass

        self.stocks = Stocks.Stocks()
        self.shitcoins = Shitcoins.Shitcoin()
        self.simplereply = Reply.SimnpleReply()
        self.misc = Misc.Misc()

        
        helper.logmessage('Successfully Loaded')



    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, **kwargs):

        #self.markAsDelivered(thread_id, message_object.id)
        self.markAsRead(thread_id)
        if str(author_id) != str(self.uid):
            chatline = str(message_object.text).lower()
            respstring = ''

            if chatline.startswith('!stock'):
                helper.logmessage('Stock request triggered')
                respstring = self.stocks.check_stock(chatline)

            elif chatline.startswith("!decide"):
                helper.logmessage('Decision Triggered')
                respstring = self.misc.decide(chatline)

            elif chatline.startswith('!math '):
                helper.logmessage('Calculation Triggered')
                respstring = self.misc.calculate(chatline)

            elif chatline.startswith('!captcha'):
                helper.logmessage('2Captcha Called')
                respstring = self.misc.get_captchacredit()

            elif "/gyazo.com/" in chatline:
                helper.logmessage('Crappy Gyazo URL')
                respstring = self.helper.anti_gyazo(chatline)

            elif chatline.startswith('!dtime ') and len(chatline.split(' ')) > 1:
                helper.logmessage('Timezone Triggered')
                respstring = self.misc.get_time(chatline)

            elif chatline.startswith('!addcmd') and len(chatline.split(' ')) > 1:
                helper.logmessage('Adding Command')
                respstring = self.simplereply.add_command(str(message_object.text))

            elif chatline.startswith('!delcmd') and len(chatline.split(' ')) > 1:
                helper.logmessage('Deleting Command')
                respstring = self.simplereply.del_command(message_object.author, chatline)

            elif chatline.startswith('!commands'):
                helper.logmessage('Command List Triggered')
                respstring = 'Commands: !addcmd <command> <response>, !captcha, !decide <1, 2, 3, ...>, !delcmd <command>, !dtime <timezone>, !math <equation>, !stock <stockcode> | '
                respstring += self.simplereply.list_commands()

            elif chatline.startswith('!'):
                messagecontent = chatline[1:]
                msg = messagecontent.split(' ')[0].upper()

                if len(msg) > 0:
                    respstring = self.simplereply.respond(msg)
                    if respstring == '':
                        respstring = self.shitcoins.get_cmcaltcoin(msg[:6])
            
            if respstring is not '':
                self.sendMessage(respstring,thread_id=thread_id,thread_type=thread_type)







#Now actually start the bot
bot = AltCoinBot(config.username, config.password, config.useragent)
bot.listen()



