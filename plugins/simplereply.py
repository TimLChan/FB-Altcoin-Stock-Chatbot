#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    FB Chatbot - Simple Reply Plugin
    ~~~~~~
    based on triggers, return a response

"""
__author__ = 'Tim Chan'
__email__ = 'github@timc.me'
__copyright__ = 'Copyright 2020 by Tim Chan'
__version__ = '1.5'
__license__ = 'MIT'


import pickle
import settings.settings as config
import plugins.common as helper

class SimnpleReply(object):

    responses = {}
    def __init__(self):
        self.load_file()
        helper.logmessage('Loaded SimpleReply Plugin')

    def save_file(self):
        with open('responses.dat', 'wb') as responsefile:
            pickle.dump(self.responses, responsefile)

    def load_file(self):
        with open('responses.dat', 'rb') as responsefile:
            try:
                self.responses = pickle.loads(responsefile.read())
            except EOFError:
                self.responses = {}

    def add_command(self, message):
        try:
            messagesplit = helper.parsemessage(message).split(' ')
            command = str(messagesplit[0]).lower()

            if command in self.responses:
                return 'Command already exists! Delete the command first using !delcmd {}'.format(command)

            response = str(" ".join(messagesplit[1:]))
            self.responses[command] = response
            self.save_file()
            return '"{}" command added to return "{}"'.format(command, response)
        except Exception as e:
            helper.logmessage('Command Addition Error: {} | Message: {}'.format(str(e), message))
            return 'Could not add command!'

    def del_command(self, fbid, message):
        if fbid in config.adminfbids:
            command = str(helper.parsemessage(message).split(' ')[0]).lower()
            if command in self.responses:
                try:
                    del self.responses[command]
                    self.save_file()
                    return 'Successfully deleted command "{}"'.format(command)
                except Exception as e:
                    helper.logmessage('Command Deletion Error: {} | Message: {}'.format(str(e), message))
                    return 'Could not delete command!'
            else:
                return 'Cannot delete what is not there!!'
        else:
            return 'NOOB U R NOT ADMIN'

    def respond(self, command):
        helper.logmessage('Simple Response Triggered')
        command = command.translate(str.maketrans('', '', '!-:.^')).lower()
        if command in self.responses:
            return self.responses[command]
        else:
            return ''

    def list_commands(self):
        respstring = 'Custom Commands: !'
        respstring += ", !".join(sorted(self.responses))
        return respstring