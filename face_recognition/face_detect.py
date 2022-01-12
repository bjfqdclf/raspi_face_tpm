import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from tengxun_cloud.face_research import face_research
import numpy as np


def cv2_add_chinese_text(img, text, position, text_color=(0, 255, 0), text_size=30):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    font_style = ImageFont.truetype("simsun.ttc", text_size, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, text_color, font=font_style)
    # 转换回OpenCV格式
    return cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)


def face_detect_demo(img, person_name):
    """检测人脸"""
    # 转为灰度图片
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 加载分类器
    face_detect = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 检测图像
    face = face_detect.detectMultiScale(gray_img, 1.1)
    # 绘制框
    text_flag = False
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
        if not text_flag:  # 只标记第一个人脸名字
            text_flag = True
            if person_name:
                img = cv2_add_chinese_text(img, person_name, (x, y - 32), (0, 255, 0))
            else:
                img = cv2_add_chinese_text(img, 'unknow', (x, y - 32), (0, 255, 0))
    cv.imshow('result', img)
    return face


def save_search(img, face_coordinate):
    """
    对人脸图像处理
    img: 图片
    face_coordinate: 人脸位置坐标
    """
    x, y, w, h = face_coordinate
    img = img[y-20:y + h + 20, x-20:x + w + 20].copy()
    return img


# 读取摄像头图像
if __name__ == '__main__':

    cap = cv.VideoCapture(0)
    face_search_lock = False
    person_id = None
    person_name = None
    face_remove_count = 0
    while True:
        flag, france = cap.read()
        if not flag:
            break
        face = face_detect_demo(france, person_name)
        if (not isinstance(face, tuple)) and (not face_search_lock) and (not person_id):
            face_search_lock = True
            face_remove_count = 0
            x, y, w, h = face[0]
            img_search = save_search(france, face[0])

            cv.imwrite('img/face_search.jpg', img_search)
            face_res = face_research('img/face_search.jpg')
            if face_res:
                person_id, person_name = face_res
        if isinstance(face, tuple):  # 未检测到人脸
            face_remove_count += 1
            if face_remove_count > 10:
                face_search_lock = False
                person_id = None
                person_name = None
        if ord('q') == cv.waitKey(5):
            break
    # 释放内存
    cv.destroyAllWindows()
    # 释放摄像头
    cap.release()
