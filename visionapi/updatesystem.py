from openvision.settings import FACENET, EMBEDDINGS, TRAINING_ROLL, DATASET
import os
import cv2
import pickle
import random
from numpy import expand_dims


def updateapi():
    from mtcnn.mtcnn import MTCNN
    import keras
    model = keras.models.load_model(FACENET)
    detector = MTCNN()
    training = []
    category = []
    for folder in os.listdir(DATASET):
        folder_path = os.path.join(DATASET, folder)
        category.append(folder)
        for file in os.listdir(folder_path):
            filepath = os.path.join(folder_path, file)
            frame = cv2.imread(filepath, 1)
            result = detector.detect_faces(frame)
            if result:
                for person in result:
                    x, y, w, h = person['box']
                    roi_gray = frame[y:y + h, x:x + w]
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 0, 255), 1)
                    cv2.imshow("frame", frame)
                    cv2.waitKey(5)
                    face = cv2.resize(roi_gray, (160, 160))
                    face = face.astype('float32')
                    mean, std = face.mean(), face.std()
                    face = (face - mean) / std
                    samples = expand_dims(face, axis=0)
                    embeddings = model.predict(samples)
                    print(embeddings)
                    training.append([embeddings, category.index(folder)])
    random.shuffle(training)
    x = []
    y = []
    for features, labels in training:
        x.append(features)
        y.append(labels)
    pickle_out = open(EMBEDDINGS, "wb")
    pickle.dump(x, pickle_out)
    pickle_out.close()
    pickle_out = open(TRAINING_ROLL, "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()
    cv2.destroyAllWindows()
