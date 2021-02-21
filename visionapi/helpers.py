import cv2
import os
from openvision.settings import UNKNOWN, IDENTIFIED
from homeview.models import Attendance, UnknownModel, User


def insertor(frame, name, unknown):
    if not unknown:
        path = os.path.join(IDENTIFIED,
                            (str(datetime.datetime.utcnow().timestamp()) + ".png"))
        cv2.imwrite(path, frame)
        user = User.objects.get(username=name)
        attendance = Attendance(user, imagePath=path)
        attendance.save()
    else:
        path = os.path.join(UNKNOWN,
                            (str(datetime.datetime.utcnow().timestamp()) + ".png"))
        cv2.imwrite(path, frame)
        unknown = UnknownModel(imagePath=path)
        unknown.save()
    print(f"date = {dt_string} Person = {name} camera_number = {camera_no}")
