import pycurl
import certifi
import io
import cv2
import numpy as np
import re
#from django.conf import settings


def get_ipaddress(value):
    """ Return IP Address array from String """
    return re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", value)


def detect_black_image(buffer):
    """ Detect Black Image. False if ALL BLACK. True if Images is NOT ALL BLACK """
    buffer.seek(0)
    file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Crop Image from center to get sample area
    w = 200
    h = 200
    height, width, channels = image.shape
    x = width/2 - w/2
    y = height/2 - h/2
    crop_image = image[int(y):int(y + h), int(x):int(x + w)]

    # Convert to Black White Image
    gray_crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
    (thresh, black_white) = cv2.threshold(gray_crop_image, 127, 255, cv2.THRESH_BINARY)

    if cv2.countNonZero(black_white) != 0:
        print("Image is fine")
        is_image_ok = True
    else:
        print("Error")
        is_image_ok = False

    return is_image_ok


def get(url):
    """ Check Channel and if picture snapshot is BLANK or not """
    buffer = io.BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CAINFO, certifi.where())
    if re.search('http://admin:', url):
        c.setopt (c.HTTPAUTH, c.HTTPAUTH_DIGEST)

    result = True
    try:
        c.perform()
    except pycurl.error:
        result = False

    c.close()

    # Detect Image Black
    is_image_ok = False
    if result and buffer.getbuffer().nbytes > 0:
        is_image_ok = detect_black_image(buffer)

    buffer.close()

    return result, is_image_ok
