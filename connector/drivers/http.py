import pycurl
import certifi
from io import BytesIO, StringIO
import cv2
import numpy as np


def get(url):
    #buffer = BytesIO()
    buffer = StringIO
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    #c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    with open('/tmp/pfm.jpg', 'w') as f:
        c.setopt(c.WRITEFUNCTION, f.write)
        try:
            c.perform()
            result = True
        except pycurl.error:
            result = False

    '''
    try:
        c.perform()
        result = True
    except pycurl.error:
        result = False
    '''

    c.close()

    ''' Detect Image Black '''
    if result:
        file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        image = cv2.imread('/tmp/pfm.jpg', 0)
        #image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gray_version = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if cv2.countNonZero(gray_version) == 0:
            print("Error")
        else:
            print("Image is fine")

        #if cv2.countNonZero(image) == 0:
        #    print("Image is black")
        #else:
        #    print("Colored image")
    else:
        pass

    buffer.close()

    return result
