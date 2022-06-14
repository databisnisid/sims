import pycurl
import certifi
import io
import cv2
import numpy as np
import re
import time


def detect_black_image(buffer):
    """ Detect Black Image. False if ALL BLACK. True if Images is NOT ALL BLACK """
    buffer.seek(0)
    file_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    gray_version = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    w = 50
    h = 50
    height, width, channels = image.shape
    print('Height', height)
    print('Width', width)
    x = width/2 - w / 2
    y = height/2 - h / 2
    print('X', x)
    print('Y', y)
    #crop_image = image[y:y + h, x:x + w]
    crop_image = image[int(y):int(y + h), int(x):int(x + w)]
    gray_crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)

    ts = time.time()
    cv2.imwrite('/tmp/yoga/test' + ts + '.jpg', gray_crop_image)


    #if cv2.countNonZero(gray_version) != 0:

    if cv2.countNonZero(gray_crop_image) != 0:
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
    #c.setopt(c.CAINFO, certifi.where())
    if re.search('http://admin', url):
        c.setopt (c.HTTPAUTH, c.HTTPAUTH_DIGEST)
        #c.setopt(c.username, "admin")
        #c.setopt(c.password, "P4ssw0rd!")
    result = True
    try:
        c.perform()
    except pycurl.error:
        result = False

    c.close()

    # Detect Image Black
    is_image_ok = False
    if result:
        is_image_ok = detect_black_image(buffer)

    buffer.close()

    return result, is_image_ok
