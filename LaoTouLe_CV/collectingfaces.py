# 采集人脸
import shutil

import cv2
import os

# 调用笔记本内置摄像头，所以参数为0，如果有其他的摄像头可以调整参数为1，2
cap = cv2.VideoCapture(0)
# 加载人脸模型库
face_detector = cv2.CascadeClassifier('./models/haarcascade_frontalface_default.xml')
face_id = input('\n 请输入姓名序号:')
print('\n 初始化面临捕获。看着镜头，等待 ...')
dirPath='./images'
# 新建目录
savePath=os.path.join(dirPath,face_id)
if os.path.exists(savePath):
    shutil.rmtree(savePath, True)

os.mkdir(savePath)
print(savePath)
count = 0
# 获取摄像头实时画面
while True:
    # 读取摄像头当前这一帧的画面  success:True False image:当前这一帧画面
    success, img = cap.read()
    if not success:  # ok 是判断你有没有得到数据
        break
    # # 转为灰度图片
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # # 检测人脸
    # faces = face_detector.detectMultiScale(gray, 1.3, 5)
    # if len(faces) > 0:
    #     for (x, y, w, h) in faces:
    #         # 画出矩形框
    #         cv2.rectangle(img, (x, y), (x+w, y+w), (255, 0, 0))
    #         count += 1
    #         # 保存图像
    cv2.imwrite(savePath +'/' + str(count) + '.jpg',img)
    count=count+1
    cv2.imshow('collecting image', img)
    # 显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(img, 'num:%d' % count, (10, 20), font, 1, (255, 0, 255), 4)
    # 保持画面的持续。
    k = cv2.waitKey(5)
    if k == 27:   # 通过esc键退出摄像
        break
    elif count >= 500:  # 得到500个样本后退出摄像
        break
# 关闭摄像头
cap.release()
# 销毁窗口
cv2.destroyAllWindows()