import cv2
import os
from openvision.settings import DATASET


def addimage(username):
    cap = cv2.VideoCapture(0)
    userpath = os.path.join(DATASET, username)
    if not os.path.isdir(userpath):
        os.makedirs(userpath)
    i = 0
    while i < 25:
        i = i + 1
        ret, image = cap.read()
        image = cv2.resize(image, (640, 480))
        image = cv2.flip(image, 1)
        cv2.imwrite((os.path.join(userpath, f"{username}-{i}.png")), image)
        cv2.imshow("frame", image)
        cv2.waitKey(200)
    cv2.destroyAllWindows()
