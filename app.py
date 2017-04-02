import fbchat
import json
import decimal
import urllib3
urllib3.disable_warnings()

#subclass fbchat.Client and override required methods
class AltCoinBot(fbchat.Client):
    httphandler = urllib3.PoolManager()
    urlau = "https://api.independentreserve.com/Public/GetMarketSummary?primaryCurrencyCode=xbt&secondaryCurrencyCode=aud"
    ctx = decimal.Context()
    ctx.prec = 20
    
    
    def float_to_str(self,f):
        """
        Convert the given float to a string,
        without resorting to scientific notation
        """
        """ Thanks to http://stackoverflow.com/posts/38847691/revisions """
        d1 = self.ctx.create_decimal(repr(f))
        return format(d1, 'f')
    
    def __init__(self,email, password, debug=False, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        print('Successfully Loaded')

    def on_message_new(self, mid, author_id, message, metadata, recipient_id, thread_type):
        self.markAsDelivered(recipient_id, mid) #mark delivered
        self.markAsRead(recipient_id) #mark read
        
        if str(author_id) != str(self.uid):
            chatline = str(message)
            if chatline.startswith('!stock'):
                    print('Stock request triggered')
                    messagecontent = chatline.split(' ')
                    if messagecontent[1] and messagecontent[1].replace('.', '').isalnum():
                        stockcode = messagecontent[1].upper()[:8]
                        respstring = ''
                        url = 'http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + stockcode + '%22)&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&format=json'
                        response = self.httphandler.request('GET', url)
                        stockchart = json.loads(response.data.decode('utf-8'))
                        stockres = stockchart['query']['results']['quote']
                        if stockres['Ask']:
                            respstring = '{} ({}) Price: ${} | Change: ${} ({})'.format(stockres['Name'], stockres['Symbol'], stockres['LastTradePriceOnly'], stockres['Change'], stockres['ChangeinPercent'])                            
                        else:
                            respstring = 'Nothing found for ' + stockcode
                        self.send(recipient_id,respstring,message_type=thread_type)
            elif chatline.startswith('!') and str(message).lower() != '!btcaud':
                messagecontent = str(message)[1:].lower()
                msg = messagecontent.split(' ')[0].upper()
                if len(msg) > 0:
                    print(msg + ' command triggered')
                    respstring = 'Current ' + msg + ' price: '
                    urlbuilder = 'https://min-api.cryptocompare.com/data/price?fsym=' + msg + '&tsyms=USD,BTC'
                    if messagecontent.endswith('poloniex'):
                        if msg == 'BTC':
                             urlbuilder = 'https://min-api.cryptocompare.com/data/price?fsym=' + msg + '&tsyms=USD&e=Poloniex'
                        else:
                            urlbuilder += '&e=Poloniex'
                        respstring = 'Current ' + msg + ' price (Poloniex): '
                    
                    response = self.httphandler.request('GET', urlbuilder)
                    btcchart = json.loads(response.data.decode('utf-8'))
                    
                    if 'Response' not in btcchart:
                        if 'USD' in btcchart:
                            respstring += self.float_to_str(btcchart['USD']) + ' USD'
                        if 'BTC' in btcchart:
                            respstring += ' | ' + self.float_to_str(btcchart['BTC']) + ' BTC'
                    else:
                        respstring = btcchart['Message']
                        
                    self.send(recipient_id,respstring,message_type=thread_type)
                
            elif chatline == '!btcaud':
                print('BTC in AUD triggered')
                response = self.httphandler.request('GET', self.urlau)
                btcchart = json.loads(response.data.decode('utf-8'))
                sendstr = 'Current BTC Price (IndependentReserve): A$' + self.float_to_str(btcchart['LastPrice'])
                self.send(recipient_id,sendstr,message_type=thread_type)
                
            

bot = AltCoinBot("<Email>", "<Password>")
bot.listen()
