import cv2
import numpy as np
import re
import pathlib
from django.conf import settings


def get_ipaddress(value):
    """ Return IP Address array from String """
    return re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", value)


def detect_black_image(image):
    """ Detect Black Image. False if ALL BLACK. True if Images is NOT ALL BLACK """
    w = 200
    h = 200
    height, width, channels = image.shape
    x = width / 2 - w / 2
    y = height / 2 - h / 2
    crop_image = image[int(y):int(y + h), int(x):int(x + w)]

    gray_crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2GRAY)
    (thresh, black_white) = cv2.threshold(gray_crop_image, 127, 255, cv2.THRESH_BINARY)

    if cv2.countNonZero(black_white) != 0:
        print("Image is fine")
        is_image_ok = True
    else:
        print("Error")
        is_image_ok = False

    return is_image_ok


def get(url, channel=1):
    """ Open RTSP stream, capture a frame, detect if black, save snapshot """
    result = True
    is_image_ok = False
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        cap.release()
        return False, False

    for _ in range(30):
        ret, frame = cap.read()
        if ret:
            break

    if ret and frame is not None:
        is_image_ok = detect_black_image(frame)

        ipaddress = get_ipaddress(url)
        if ipaddress:
            media_path = settings.MEDIA_ROOT + '/camera'
            pathlib.Path(media_path).mkdir(parents=True, exist_ok=True)
            image_path = media_path + '/' + ipaddress[0] + '_' + str(channel) + '.png'
            cv2.imwrite(image_path, frame)
    else:
        result = False

    cap.release()
    return result, is_image_ok
