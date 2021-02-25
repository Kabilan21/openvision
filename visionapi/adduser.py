import cv2
import os
import urllib.request as ur
import numpy as np
from openvision.settings import DATASET, USE_INTEGERATED_WEB_CAM, REMOTE_CAM_URL


def addimage(username):
    cap = cv2.VideoCapture(0)
    userpath = os.path.join(DATASET, username)
    if not os.path.isdir(userpath):
        os.makedirs(userpath)
    i = 0
    while i < 50:
        i = i + 1
        if USE_INTEGERATED_WEB_CAM:
            _, frame = cap.read()
        else:
            imgResp = ur.urlopen(REMOTE_CAM_URL)
            imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgNp, -1)
        try:
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.flip(frame, 1)
        except:
            continue
        cv2.imwrite((os.path.join(userpath, f"{username}-{i}.png")), frame)
        cv2.imshow("frame", frame)
        cv2.waitKey(500)
    cv2.destroyAllWindows()
