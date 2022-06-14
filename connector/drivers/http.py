import pycurl
import certifi
from io import BytesIO, StringIO
import cv2
import numpy as np


def get(url):
    """ Check Channel and if picture snapshot is BLANK or not """
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

    ''' Detect Image Black '''
    if result:
        buffer.seek(0)
        file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        gray_version = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if cv2.countNonZero(gray_version) == 0:
            print("Error")
            is_image_ok = False
        else:
            print("Image is fine")
            is_image_ok = True

    buffer.close()

    return result, is_image_ok
