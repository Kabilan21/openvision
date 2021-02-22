import cv2
import os
from openvision.settings import UNKNOWN, IDENTIFIED, identified, unknown
from homeview.models import Attendance, UnknownModel, User
import datetime


def insertor(frame, name, unknowns):
    current_time = (str(datetime.datetime.utcnow().timestamp()) + ".png")
    if not unknowns:
        path = os.path.join(IDENTIFIED,
                            current_time)
        cv2.imwrite(path, frame)
        user = User.objects.get(username=name)
        attendance = Attendance(
            user=user, imagePath=f"{identified}/{current_time}")
        attendance.save()
        print(name)
    else:
        path = os.path.join(UNKNOWN,
                            current_time)
        cv2.imwrite(path, frame)
        unknown = UnknownModel(imagePath=f"{unknown}/{current_time}")
        unknown.save()
