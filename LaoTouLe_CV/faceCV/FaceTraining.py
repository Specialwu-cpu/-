# 人脸数据训练
import numpy as np
from PIL import Image
import os
import cv2

# 人脸数据路径
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("../models/haarcascade_frontalface_default.xml")


def getImagesAndLabels(path):
    dirPaths = [os.path.join(path, f) for f in os.listdir(path)]  # join函数的作用？
    faceSamples = []
    ids = []
    for imagePaths in dirPaths:
        id = int(imagePaths.split('\\')[1])

        for imagePath in os.listdir(imagePaths):
            PIL_img = Image.open(os.path.join(imagePaths, imagePath)).convert('L')  # convert it to grayscale
            img_numpy = np.array(PIL_img, 'uint8')
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x: x + w])
                ids.append(id)
    return faceSamples, ids


print('Training faces. It will take a few seconds. Wait ...')
faces, ids = getImagesAndLabels('../images')
print(len(faces))
print(np.array(ids))

recognizer.train(faces, np.array(ids))
recognizer.write('../models/face_recognizer.yml')
print("{0} faces trained. Exiting Program".format(len(np.unique(ids))))
