import multiprocessing
import cv2
import pickle
import numpy as np
from numpy import expand_dims
from sklearn import svm
import os
import urllib.request as ur
from openvision.settings import FACENET, EMBEDDINGS, TRAINING_ROLL, DATASET, USE_INTEGERATED_WEB_CAM, REMOTE_CAM_URL
from sklearn.preprocessing import Normalizer
from homeview.models import Attendance, User
from visionapi.helpers import insertor
import json


def check():
    pickle_in = open(EMBEDDINGS, "rb")
    X = pickle.load(pickle_in)
    pickle_in = open(TRAINING_ROLL, "rb")
    encoder = Normalizer(norm='l2')
    Y = pickle.load(pickle_in)
    x = []
    names = []
    image_count = 0
    for i in os.listdir(DATASET):
        img_dir = os.path.join(DATASET, i)
        names.append(i)
        for _ in os.listdir(img_dir):
            image_count = image_count + 1
    for i in X:
        x.append(encoder.transform(i))
    clf = svm.SVC(kernel='linear', probability=True)
    x = np.array(x).reshape(len(Y), 1 * 128)
    clf.fit(x, Y)
    from tensorflow import keras
    from mtcnn.mtcnn import MTCNN
    detector = MTCNN()
    model = keras.models.load_model(FACENET)
    if USE_INTEGERATED_WEB_CAM:
        cap = cv2.VideoCapture(0)
    cv2.namedWindow(f"camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow(f"camera", 640, 480)
    controller = open("files/controller.json")
    data = json.load(controller)
    while True:
        controller = open("files/controller.json")
        data = json.load(controller)
        if not data['status']:
            cap.release()
            cv2.destroyAllWindows()
            break
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
        result = detector.detect_faces(frame)
        if result:
            for person in result:
                x, y, w, h = person['box']
                roi_gray = frame[y:y + h, x:x + w]
                try:
                    face = cv2.resize(roi_gray, (160, 160))
                except:
                    continue
                face = face.astype('float32')
                mean, std = face.mean(), face.std()
                face = (face - mean) / std
                samples = expand_dims(face, axis=0)
                embeddings = model.predict(samples)
                embeddings = encoder.transform(embeddings)
                embeddings = np.array(embeddings).reshape(1, 1 * 128)
                n = clf.predict_proba(embeddings)
                o = []
                for i in n:
                    for l in i:
                        o.append(l)
                if max(o) > 0.95:
                    insertor(frame,
                             names[o.index(max(o))], False)
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(frame, names[o.index(
                        max(o))], (x, y), font, 1, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                else:
                    if max(o) < 0.40:
                        insertor(frame, "unknown", True)
                        font = cv2.FONT_HERSHEY_COMPLEX
                        cv2.putText(frame, "Unknown", (x, y), font,
                                    1, (0, 0, 255), 1, lineType=cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.imshow(f"camera", frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
