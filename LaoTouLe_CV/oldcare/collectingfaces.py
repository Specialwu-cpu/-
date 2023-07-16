'''
图像采集程序-人脸检测
由于外部程序需要调用它，所以不能使用相对路径

用法：
python collectingfaces.py --id 106 --imagedir /home/reed/git-project/
    old_care_system/任务源代码/任务 5.老人员工义工人脸图像采集/images
    id和imagedir自己设置
from xiaoyi.zhang:以上调用方法为基于linux系统的方式，windows是否可以这样调用未知，需研究
'''

import argparse
from facial import FaceUtil
from audio import audioplayer
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import os
import shutil
import time

# 全局参数
# 音频文件所在文件目录，文档里是linux的方式，这个用不上，我在play_audio函数内部加了文件路径，不用传入了
# audio_dir = 'imagedir/home/reed/git-project/old_care_system/任务源代码/任务 5.老人员工义工人脸图像采集/audios'


# 控制参数
error = 0
start_time = None
limit_time = 2 # 2 second

# 传入参数, 需要前端传入imagedir和id用于保存采集到的图像
ap = argparse.ArgumentParser()
ap.add_argument("-ic", "--id", required=True, help="")
ap.add_argument("-id", "--imagedir", required=True,
                help="")
args = vars(ap.parse_args())

action_list = ['blink', 'open_mouth', 'smile', 'rise_head',
               'bow_head', 'look_left', 'look_right']
action_map = {
    'blink': '请眨眼',
    'open_mouth': '请张嘴',
    'smile': '请笑一笑',
    'rise_head': '请抬头',
    'bow_head': '请低头',
    'look_left': '请看左边',
    'look_right': '请看右边'
}
# 设置摄像头
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

faceutil = FaceUtil()
counter = 0

while True:
    counter += 1
    _, image = cam.read()
    if counter <= 10: # 放弃前10帧
        continue
    image = cv2.flip(image, 1)

    if error == 1:
        end_time = time.time()
        difference = end_time - start_time
        print(difference)
        if difference >= limit_time:
            error = 0

    face_location_list = faceutil.get_face_location(image)
    for(left, top, right, bottom) in face_location_list:
        cv2.rectangle(image, (left, top, right, bottom),
                      (0, 0, 255), 2)

    cv2.imshow('Collecting Faces', image) # show the image
    # press 'ESC' for exiting video
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

    face_count = len(face_location_list)
    if error == 0 and face_count == 0: # 没有检测到人脸
        print('[WARNING] 没有检测到人脸')
        audioplayer.play_audio('no_face_detected')
        error = 1
        start_time = time.time()
    elif error == 0 and face_count == 1: # 可以开始采集图像了
        print('[INFO] 可以采集图像了')
        audioplayer.play_audio('start_image_capturing')
        break
    elif error == 0 and face_count > 1: # 检测到多张人脸
        print('[WARNING] 检测到多张人脸')
        audioplayer.play_audio('multi_faces_detected')
        error = 1
        start_time = time.time()
    else:
        pass


# 新建目录
if os.path.exists(os.path.join(args['imagedir'], args['id'])):
    shutil.rmtree(os.path.join(args['imagedir'], args['id']), True)
os.mkdir(os.path.join(args['imagedir'], args['id']))

# 开始采集人脸
for action in action_list:
    audioplayer.play_audio(action)
    action_name = action_map[action]

    counter = 1
    for i in range(15):
        print('%s-%d' %(action_name, i))
        _, img_OpenCV = cam.read()
        img_OpenCV = cv2.flip(img_OpenCV, 1)
        origin_img = img_OpenCV.copy()  # 保存时使用

        face_location_list = faceutil.get_face_location(img_OpenCV)
        for(left, top, right, bottom) in face_location_list:
            cv2.rectangle(img_OpenCV, (left, top, right, bottom), (0, 0, 255), 2)

        img_PIL = Image.fromarray(cv2.cvtColor(img_OpenCV, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_PIL)
        draw.text((int(image.shape[1]/2), 30), action_name,
                  font=ImageFont.truetype('simhei.ttf', 40),
                  fill=(255, 0, 0)) # linux <-注释写了linux，但是问了gpt说是可以在windows上跑
        # 转回OpenCV格式
        img_OpenCV = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        cv2.imshow('Collecting Faces', img_OpenCV)  # show the image
        image_name = os.path.join(args['imagedir'], args['id'],
                                  action+'_'+str(counter)+'.jpg')
        cv2.imwrite(image_name, origin_img)
        # press 'ESC' for exiting video
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        counter += 1

# 结束
print('[INFO] 采集完毕')
audioplayer.play_audio('end_capturing')

# 释放全部资源
cam.release()
cv2.destroyAllWindows()