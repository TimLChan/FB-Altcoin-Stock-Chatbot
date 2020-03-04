import decimal
import re
from datetime import datetime

ctx = decimal.Context()


def float_to_str(f, prec):
    """
    Convert the given float to a string,
    without resorting to scientific notation
    Thanks to http://stackoverflow.com/posts/38847691/revisions
    """
    f = float(f)
    ctx.prec = prec
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

def logmessage(msg):
    print(('[{}] {}').format(datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'), msg))


def parsemessage(message):
    return ' '.join(message.split(' ')[1:])

def anti_gyazo(url):
    newurl = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    newurl = newurl.group()
    newurl = newurl.replace("gyazo.com","i.gyazo.com")
    newurl += ".png"
    return 'URL for mobile users: ' + newurl