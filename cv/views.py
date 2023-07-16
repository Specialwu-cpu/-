from django.shortcuts import render

from LaoTouLe_CV.faceCV import FaceCV

import threading
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import cv2
from django.http import StreamingHttpResponse

from LaoTouLe_CV.fall_detection import FallDetection


def gen_display(camera):
    """
    视频流生成器功能。
    """
    cv = FaceCV(0)
    while True:
        ret, frame = cv.start(1)
        # if ret:
        # 将图片进行解码
        # ret, frame = cv2.imencode('.jpeg', frame)
        if ret:
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
    # temp = FaceCV(0)
    # while True:
    #     temp.start(0)
    #     k = cv2.waitKey(5) & 0xff
    #     if k == 27:
    #         temp.end()
    #         break
    # while True:
    #     # 读取图片
    #     ret, frame = camera.read()
    #     if ret:
    #         # 将图片进行解码
    #         ret, frame = cv2.imencode('.jpeg', frame)
    #         if ret:
    #             # 转换为byte类型的，存储在迭代器中
    #             yield (b'--frame\r\n'
    #                    b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@csrf_exempt
def face_video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象
    cameraId = 0
    # camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(gen_display(cameraId), content_type='multipart/x-mixed-replace; boundary=frame')


def fall_down_display(camera):
    """
    视频流生成器功能。
    """
    fd = FallDetection(0)
    while True:
        ret, frame = fd.detect(1)
        # if ret:
        # 将图片进行解码
        # ret, frame = cv2.imencode('.jpeg', frame)
        if ret:
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@csrf_exempt
def fall_down_video(request):
    """
    视频流路由。将其放入img标记的src属性中。
    例如：<img src='https://ip:port/uri' >
    """
    # 视频流相机对象
    cameraId = 0
    # camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(fall_down_display(cameraId), content_type='multipart/x-mixed-replace; boundary=frame')


# @csrf_exempt
# def face_cv(request):
#     if request.method == 'GET':
#         def algorithm_thread():
#             cv = FaceCV()
#             while True:
#                 cv.start()
#                 k = cv2.waitKey(5) & 0xff
#                 if k == 27:
#                     cv.end()
#                     break
#
#         thread = threading.Thread(target=algorithm_thread)
#         thread.start()
#
#         return JsonResponse({'message': 'Algorithm started'})
#     else:
#         return JsonResponse({'message': 'only GET method is allowed'})


def fire_detection_display(cameraId):
    """
        视频流生成器功能。
        """
    fd = FallDetection(0)
    while True:
        ret, frame = fd.detect(1)
        # if ret:
        # 将图片进行解码
        # ret, frame = cv2.imencode('.jpeg', frame)
        if ret:
            # 转换为byte类型的，存储在迭代器中
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')


@csrf_exempt
def fire_detection(request):
    """
        视频流路由。将其放入img标记的src属性中。
        例如：<img src='https://ip:port/uri' >
        """
    # 视频流相机对象
    cameraId = 0
    # camera = cv2.VideoCapture(0)
    # 使用流传输传输视频流
    return StreamingHttpResponse(fire_detection_display(cameraId), content_type='multipart/x-mixed-replace; boundary=frame')
