#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Chatbot - Miscellaneous Plugin
    ~~~~~~
    Miscellaneous functions

"""

__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2022 by Tim Chan'
__version__ = '2.0'
__license__ = 'MIT'


import json
import random
import datetime
import re 

import settings.settings as config
import plugins.common as helper

class Misc(object):

    def __init__(self):
        helper.logmessage('Loaded Misc plugin')

    def decide(self, message):
        decisions = helper.parsemessage(message).split(',')
        helper.logmessage(decisions)
        kinda_random = random.SystemRandom()
        return 'Decision: {}'.format(kinda_random.choice(decisions).strip())

    def get_captchacredit(self):
        respstring = 'Current 2Captcha balance: $'
        response = helper.sendget(config.twocaptchaapi.format(config.twocaptchakey))
        respstring += response.text
        return respstring

    def calculate(self, message):
        parsedmsg = helper.parsemessage(message)
        equation = re.sub(r'[^\d\.+^\-\/\*]+', '', parsedmsg)
        try:
            if len(equation) < 3:
                raise ValueError
            encodeddata = helper.urlsafe(equation)
            answer = helper.sendget(config.mathapi.format(encodeddata))
            return '{} = {}'.format(parsedmsg, answer.text)
        except:
            return 'BAD INPUT WTF'

    def get_time(self, message):
        try:
            timezone = int(helper.parsemessage(message))
        except:
            timezone = 999
        try:

            if -13 <= timezone <= 14:
                utc_datetime = datetime.datetime.utcnow()
                result_utc_datetime = utc_datetime + datetime.timedelta(hours=int(timezone))
                respstring = 'Time for GMT {}: {}'.format(timezone, result_utc_datetime.strftime("%a %d %B - %I:%M%p"))
            else:
                respstring = 'Error: Choose a timezone between UTC-13 and UTC+14'
        except Exception as e:
            helper.logmessage('Exception while getting time. Exception: {}'.format(str(e)))
            respstring = 'FUARK error'

        return respstring
