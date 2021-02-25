import cv2
import os
from openvision.settings import UNKNOWN, IDENTIFIED, identified, unknown
from homeview.models import Attendance, UnknownModel, User
from datetime import datetime, timedelta


def insertor(frame, name, unknowns):
    time_threshold = datetime.now() - timedelta(minutes=5)
    current_time = (str(datetime.utcnow().timestamp()) + ".png")
    if not unknowns:
        print(name)
        user = User.objects.get(username=name)
        attendance = Attendance.objects.filter(user=user,
                                               timestamp__gt=time_threshold).first()
        if attendance is None:
            path = os.path.join(IDENTIFIED,
                                current_time)
            cv2.imwrite(path, frame)
            attendance = Attendance(
                user=user, imagePath=f"{identified}/{current_time}")
            attendance.save()
            print("adding data")
        else:
            print("not adding")
        print(name)
    else:
        time_threshold = datetime.now() - timedelta(seconds=30)
        present = UnknownModel.objects.filter(
            timestamp__gt=time_threshold).first()
        if present is None:
            path = os.path.join(UNKNOWN,
                                current_time)
            cv2.imwrite(path, frame)
            unknownmodel = UnknownModel(imagePath=f"{unknown}/{current_time}")
            unknownmodel.save()
            print("adding unknown")
        else:
            print("unknown already present")
