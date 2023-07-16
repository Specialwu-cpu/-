'''
陌生人识别模型和情感分析模型的结合的主程序
'''

# 导入包
import argparse
import datetime

from PIL import Image, ImageDraw, ImageFont

from keras.models import load_model
from tensorflow.keras.utils import img_to_array
import cv2
import time
import numpy as np
import os
import imutils
import subprocess
from scipy.spatial import distance as dist

from event_info.views import insert_event


# 转换为PIL的image图片格式,使用PIL绘制文字,再转换为OpenCV的图片格式
def image_add_text(img1, text, left, top, text_color, text_size):
    # 判断图片是否为ndarray格式，转为成PIL的格式的RGB图片
    if isinstance(img1, np.ndarray):
        image = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(image)
    # 参数依次为 字体、字体大小、编码
    font_style = ImageFont.truetype("../LaoTouLe_CV/font/MSYH.TTC", text_size, encoding='utf-8')
    # 参数依次为位置、文本、颜色、字体
    draw.text((left, top), text, text_color, font=font_style)
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


class FaceCV:
    def __init__(self, cameraId):

        # TODO
        # 全局变量
        self.facial_expression_model_path = '../LaoTouLe_CV/models/emotion_model.hdf5'
        self.facial_recognize_model_path = 'D:\projects\happyOlder\server\LaoTouLe_CV\models\\face_recognizer.yml'
        self.output_stranger_path = 'D:/projects/happyOlder/server/LaoTouLe_CV/supervision/strangers/'
        self.output_smile_path = 'D:/projects/happyOlder/server/LaoTouLe_CV/supervision/smile/'
        self.cascadePath = "../LaoTouLe_CV/models/haarcascade_frontalface_default.xml"
        # 这是根据csv提取名称和对应信息的，但是这里直接写死了
        # people_info_path = 'info/people_info.csv'
        # facial_expression_info_path = 'info/facial_expression_info.csv'
        self.typeId_to_typeName = {'Unknown': '陌生人', 1: '老人', 2: '老人', 3: '志愿者'}
        self.id_to_name = {1: '陈航', 2: '吴书海', 3: '郑若翀'}
        self.id_to_typeId = {'Unknown': 'Unknown', 1: 1, 2: 2, 3: 3}
        self.facial_expression_id_to_name = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy',
                                             4: 'Sad', 5: 'Surprise', 6: 'Neutral'}
        # 全局常量

        self.FACIAL_EXPRESSION_TARGET_WIDTH = 28
        self.FACIAL_EXPRESSION_TARGET_HEIGHT = 28

        self.VIDEO_WIDTH = 640
        self.VIDEO_HEIGHT = 480
        self.FACE_ACTUAL_WIDTH = 20
        self.ACTUAL_DISTANCE_LIMIT = 100
        # ANGLE = 20
        if not os.path.exists(self.output_smile_path):
            os.makedirs(self.output_smile_path)

        if not os.path.exists(self.output_stranger_path):
            os.makedirs(self.output_stranger_path)

        # 控制陌生人检测
        self.strangers_timing = 0  # 计时开始
        self.strangers_start_time = 0  # 开始时间
        self.strangers_limit_time = 3  # if >= 3 seconds, then he/she is a stranger.

        # 控制情感分析
        self.facial_expression_timing = 0  # 计时开始
        self.facial_expression_start_time = 0  # 开始时间
        self.facial_expression_limit_time = 3  # if >= 3 seconds, he/she is smiling

        self.vs = cv2.VideoCapture(cameraId)
        time.sleep(2)
        self.facial_expression_model = load_model(self.facial_expression_model_path)
        self.emotion_target_size = self.facial_expression_model.input_shape[1:3]
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(self.facial_recognize_model_path)

        self.faceCascade = cv2.CascadeClassifier(self.cascadePath)
        # # 得到画面的四分之一位置和四分之三位置
        self.one_fourth_image_center = (int(self.VIDEO_WIDTH / 4),
                                        int(self.VIDEO_HEIGHT / 4))
        self.three_fourth_image_center = (int(self.VIDEO_WIDTH / 4 * 3),
                                          int(self.VIDEO_HEIGHT / 4 * 3))
        # 得到当前时间
        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                          time.localtime(time.time()))
        print('[INFO] %s 陌生人检测程序和表情检测程序启动了.' % (self.current_time))

        print('[INFO] 开始检测陌生人和表情...')
        # 不断循环
        self.counter = 0

    def start(self, mode):

        self.counter += 1
        # grab the current frame
        (grabbed, frame) = self.vs.read()

        frame = cv2.flip(frame, 1)

        # frame = imutils.resize(frame, width=self.VIDEO_WIDTH,
        #                        height=self.VIDEO_HEIGHT)  # 压缩，加快识别速度
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(0.1 * self.vs.get(3)), int(0.1 * self.vs.get(4)))
        )
        volunteer_name_direction_dict = {}
        volunteer_centroids = []
        old_people_centroids = []
        old_people_name = []

        for (x, y, w, h) in faces:
            left = x
            right = x + w
            bottom = y
            top = y + h
            roi = gray[bottom:top, left:right]
            num, confidence = self.recognizer.predict(roi)
            name = 'Unknown'
            typeId = 'Unknown'
            typeName = 'Unknown'
            if confidence < 100:
                name = self.id_to_name[num]
                typeId = self.id_to_typeId[num]
                typeName = self.typeId_to_typeName[typeId]
            else:
                name = "Unknown"
            # 将人脸框出来
            rectangle_color = (0, 0, 255)
            if typeName == '老人':
                rectangle_color = (0, 0, 128)
            elif typeName == '员工':
                rectangle_color = (255, 0, 0)
            elif typeName == '志愿者':
                rectangle_color = (0, 255, 0)
            else:
                pass
            cv2.rectangle(frame, (left, bottom), (right, top),
                          rectangle_color, 2)
            facial_expression_label = ''
            # 对象是陌生人
            if name == 'Unknown':
                if self.strangers_timing == 0:  # just start timing
                    self.strangers_timing = 1
                    self.strangers_start_time = time.time()
                else:  # already started timing
                    self.strangers_end_time = time.time()
                    difference = self.strangers_end_time - self.strangers_start_time

                    self.current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                      time.localtime(time.time()))

                    if difference < self.strangers_limit_time:
                        print('[INFO] %s, 房间, 陌生人仅出现 %.1f 秒. 忽略.'
                              % (self.current_time, difference))
                    else:  # strangers appear
                        event_desc = '陌生人出现!!!'
                        event_location = '房间'
                        print('[EVENT] %s, 房间, 陌生人出现!!!'
                              % (self.current_time))
                        self.strangers_timing=0
                        # 将事件写入数据库
                        insert_event("陌生人", datetime.datetime.now(), event_location, event_desc, -1)
                        cv2.imwrite(os.path.join(self.output_stranger_path,
                                                 'snapshot_%s.jpg'
                                                 % (time.strftime('%Y%m%d_%H%M%S'))), frame)
                        # 开始陌生人追踪
                        unknown_face_center = (int((right + left) / 2),
                                               int((top + bottom) / 2))
                        cv2.circle(frame, (unknown_face_center[0],
                                           unknown_face_center[1]), 4, (0, 255, 0), -1)
                        direction = ''
                        # face locates too left, servo need to turn right,
                        # so that face turn right as well
                        if unknown_face_center[0] < self.one_fourth_image_center[0]:
                            direction = 'right'
                        elif unknown_face_center[0] > self.three_fourth_image_center[0]:
                            direction = 'left'

                        # adjust to servo
                        if direction:
                            print('%d-摄像头需要 turn %s ' % (self.counter,
                                                              direction))
            else:  # everything is ok
                strangers_timing = 0

            # 对象是老人
            if name != 'Unknown' and typeName == '老人':
                old_people_face_center = (int((right + left) / 2),
                                          int((top + bottom) / 2))
                old_people_centroids.append(old_people_face_center)
                old_people_name.append(name)

                cv2.circle(frame,
                           (old_people_face_center[0],
                            old_people_face_center[1]),
                           4, (0, 255, 0), -1)

                facial_expression_label = ''
                # 表情检测逻辑

                roi = cv2.resize(roi, self.emotion_target_size)
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # # determine facial expression
                # (neural, smile) = facial_expression_model.predict(roi)[0]
                emotion_prediction = self.facial_expression_model.predict(roi)
                emotion_label_arg = np.argmax(emotion_prediction)
                facial_expression_label = self.facial_expression_id_to_name[emotion_label_arg]
                if facial_expression_label == 'Happy':  # alert
                    if self.facial_expression_timing == 0:  # just start timing
                        self.facial_expression_timing = 1
                        self.facial_expression_start_time = time.time()
                    else:  # already started timing
                        self.facial_expression_end_time = time.time()
                        difference = self.facial_expression_end_time - self.facial_expression_start_time
                        self.current_time = time.strftime('%Y-%m-%d %H:%M:%S',
                                                          time.localtime(time.time()))
                        print('difference')
                        print(difference)
                        if difference < self.facial_expression_limit_time:
                            print('[INFO] %s, 房间, %s仅笑了 %.1f 秒. 忽略'
                                  % (self.current_time,
                                     name, difference))
                        else:  # he/she is really smiling
                            event_desc = '%s正在笑' % (name)
                            event_location = '房间'
                            self.facial_expression_timing=0
                            # 将事件写入数据库

                            insert_event("老人笑了", datetime.datetime.now(), event_location, event_desc, num)
                            print('[EVENT] %s, 房间, %s正在笑.'
                                  % (self.current_time, name))
                            cv2.imwrite(os.path.join(self.output_smile_path,
                                                     'snapshot_%s.jpg'
                                                     % (time.strftime('%Y%m%d_%H%M%S'))), frame)


                else:
                    facial_expression_timing = 0

            # 对象是志愿者
            if name != 'Unknown' and typeName == '志愿者':
                volunteer_face_center = (int((right + left) / 2),
                                         int((top + bottom) / 2))
                volunteer_centroids.append(volunteer_face_center)

                cv2.circle(frame,
                           (volunteer_face_center[0],
                            volunteer_face_center[1]),
                           8, (255, 0, 0), -1)

            final_label = name + ': '
            if facial_expression_label:
                final_label += facial_expression_label
            else:
                final_label += typeName
            print(final_label)

            frame = image_add_text(frame, final_label, left, top - 30, (255, 0, 0), 20)

        if len(faces) > 0:
            face_pixel_width = sum([i[2] for i in faces]) / len(faces)
            # 在义工和老人之间划线
            for i in volunteer_centroids:
                for j_index, j in enumerate(old_people_centroids):
                    pixel_distance = dist.euclidean(i, j)

                    pixel_per_metric = face_pixel_width / self.FACE_ACTUAL_WIDTH
                    actual_distance = pixel_distance / pixel_per_metric
                    print(actual_distance)
                    if actual_distance < self.ACTUAL_DISTANCE_LIMIT:
                        cv2.line(frame, (int(i[0]), int(i[1])),
                                 (int(j[0]), int(j[1])), (255, 0, 255), 2)
                        label = 'distance: %dcm' % (actual_distance)
                        cv2.putText(frame, label, (frame.shape[1] - 150, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                    (0, 0, 255), 2)

        if mode == 0:
            # show our detected faces along with smiling/not smiling labels
            cv2.imshow("Checking Strangers and Ole People's Face Expression",
                       frame)
        else:
            ret, frame = cv2.imencode('.jpeg', frame)
            if ret:
                return ret, frame

    def end(self):
        # cleanup the camera and close any open windows
        self.vs.release()
        cv2.destroyAllWindows()

# temp = FaceCV(0)
# while True:
#     temp.start(0)
#     k = cv2.waitKey(5) & 0xff
#     if k == 27:
#         temp.end()
#         break
