import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from tengxun_cloud.face_research import face_research
import numpy as np


class FaceServer:
    WAIT_KEY = 16

    face_search_lock = False
    person_id = None
    person_name = None
    face_remove_count = 0
    last_face = None
    now_face = None

    def __init__(self):
        try:
            self.cap = cv.VideoCapture(0)  # 打开默认摄像头
        except Exception as err:
            print(err)

        self.face_start()

    def face_start(self):
        while True:
            flag, france = self.cap.read()
            if not flag:
                break
            face = self.face_detect_demo(france)

            if isinstance(face, tuple):  # 未检测到人脸
                self.face_remove_count += 1
                if self.face_remove_count > 10:
                    self.face_search_lock = False
                    self.person_id = None
                    self.person_name = None

                if ord('q') == cv.waitKey(self.WAIT_KEY):
                    break
                continue

            # 是否换人
            self.now_face = face[0]
            is_same_face = self.same_face()
            if not is_same_face and self.face_search_lock:
                self.face_search_lock = False
                self.person_id = None
                self.person_name = None

            if (not self.face_search_lock) and (not self.person_id):
                x, y, w, h = self.now_face
                img_search = self.save_search(france)
                cv.imwrite('img/face_search.jpg', img_search)
                face_res = face_research('img/face_search.jpg')
                if face_res:  # 匹配到人脸
                    self.person_id, self.person_name = face_res
                    self.face_search_lock = True
                    self.face_remove_count = 0
                    self.last_face = self.now_face

            if ord('q') == cv.waitKey(self.WAIT_KEY):
                break
        # 释放内存
        cv.destroyAllWindows()
        # 释放摄像头
        self.cap.release()

    def face_detect_demo(self, img):
        """检测人脸"""
        # 转为灰度图片
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 加载分类器
        face_detect = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
        # 检测图像
        face = face_detect.detectMultiScale(gray_img, 1.1, 5)
        # 绘制框
        text_flag = False
        for x, y, w, h in face:
            cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
            if not text_flag:  # 只标记第一个人脸名字
                text_flag = True
                if self.person_name:
                    img = self._cv2_add_chinese_text(img, self.person_name, (x, y - 32), (0, 255, 0))
                else:
                    img = self._cv2_add_chinese_text(img, '未知', (x, y - 32), (0, 255, 0))
        cv.imshow('result', img)
        return face

    def save_search(self, img):
        """
        对人脸图像处理
        img: 图片
        face_coordinate: 人脸位置坐标
        """
        x, y, w, h = self.now_face
        img = img[y - 20:y + h + 20, x - 20:x + w + 20].copy()
        return img

    def same_face(self, size_threshold=0.2, location_threshold=10):
        """
        检测是否为同一个人
        now_face: 本帧人脸位置信息
        last_face: 上一帧人脸位置信息
        size_threshold: 大小阈值
        location_threshold: 位移阈值

        设置人脸框大小变化阈值：如宽度高度超出阈值则判定不为同一个个人
            前后面积比值

        设置位移阈值：超出位移阈值则判定不为同一个个人
        """

        if self.last_face is None:
            return True
        if self.now_face is None:
            return False

        last_x, last_y, last_w, last_h = self.last_face
        now_x, now_y, now_w, now_h = self.now_face

        # 面积判定 百分比
        face_area_percentage = (now_h * now_w) / (last_h * last_w)
        if face_area_percentage < (1 - size_threshold) or face_area_percentage > (1 + size_threshold):
            return False
        # 位置判定

        return True

    @staticmethod
    def _cv2_add_chinese_text(img, text, position, text_color=(0, 255, 0), text_size=30):
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
