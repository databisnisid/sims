import pycurl
import certifi
from io import BytesIO
#import codecs


def get(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    try:
        c.perform()
        result = True
    except pycurl.error:
        result = False

    c.close()

    if result:
        body = buffer.getvalue()
        #print(codecs.decode(body))
        print(body.decode('utf-8'))
    else:
        pass

    return result
