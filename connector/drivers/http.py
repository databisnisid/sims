import pycurl
import certifi
from io import BytesIO
import cv2


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

    ''' Detect Image Black '''
    if result:
        image = cv2.imread(buffer.write(), 0)
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
