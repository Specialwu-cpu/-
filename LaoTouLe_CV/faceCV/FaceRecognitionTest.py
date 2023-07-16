# 人脸识别
# coding=utf-8
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont

# 解决cv2.putText绘制中文乱码
def cv2ImgAddText(img2, text, left, top, textColor=(0, 0, 255), textSize=20):
    if isinstance(img2, numpy.ndarray):  # 判断是否OpenCV图片类型
        img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img2)
    # 字体的格式
    fontStyle = ImageFont.truetype('../font/MSYH.TTC', textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(numpy.asarray(img2), cv2.COLOR_RGB2BGR)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('../models/face_recognizer.yml')
cascadePath = "../models/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
num = 0
names = ['尼古拉斯·赵四', '陈航', '吴书海', '郑若翀']
cam = cv2.VideoCapture(0)
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        num, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        print(num)
        if confidence < 60:
            name = names[num]
            # confidence = "{0}%".format(round(100 - confidence))
            # confidence = format(round(100 - confidence))
        else:
            name = "unknown"
            # confidence = "{0}%".format(round(100 - confidence))
            # confidence = format(round(100 - confidence))
        # 解决cv2.putText绘制中文乱码
        img = cv2ImgAddText(img, name, x + 5, y - 30)

    cv2.imshow('camera', img)
    k = cv2.waitKey(5)
    if k == 27:
        break
cam.release()
cv2.destroyAllWindows()