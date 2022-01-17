import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from face_recognition.face_search import face_search
import numpy as np
from base.log_server import LogServer
from base.conf_obtain import sys_config
from tem_measure.temp_comp_model import TempComp
from tem_measure.temp_driver_model import enable_temp_driver


class FaceServer:
    DEVICE_id = sys_config.device_id
    WAIT_KEY = 16
    log = LogServer('img_processing')

    face_search_lock = False
    is_temp = False
    person_id = None
    person_name = None
    face_remove_count = 0
    last_face = None
    now_face = None

    def __init__(self):
        try:
            self.cap = cv.VideoCapture(0)  # 打开默认摄像头
        except Exception as err:
            self.log.error(err)

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
                    self.init_all_static_var()

                if ord('q') == cv.waitKey(self.WAIT_KEY):
                    self.log.info('程序退出...')
                    break
                continue

            # 是否换人
            self.now_face = face[0]
            is_same_face = self.same_face()
            if not is_same_face and self.face_search_lock:
                self.init_all_static_var()

            if (not self.face_search_lock) and (not self.person_id):
                x, y, w, h = self.now_face
                img_search = self.save_search(france)
                cv.imwrite('img/face_search.jpg', img_search)
                face_res = face_search('img/face_search.jpg')
                if face_res:  # 匹配到人脸
                    self.person_id, self.person_name = face_res
                    self.face_search_lock = True
                    self.face_remove_count = 0
                    self.last_face = self.now_face
                    self.log.info(f'检测到{self.person_name}')
            if self.person_id and not self.is_temp:
                # 温度检测
                try:
                    obj_temp = enable_temp_driver.get_obj_temp()  # 测量温度
                    outside_temp = enable_temp_driver.get_outside_temp()  # 环境温度
                    # 根据系统配置决定是否需要补偿
                    person_temp = self.temp_compensation(obj_temp, outside_temp)
                    if person_temp:
                        # 存数据库 TODO
                        self.data_save()
                        self.is_temp = True

                except Exception as err:
                    self.log.error(err)

            if ord('q') == cv.waitKey(self.WAIT_KEY):
                self.log.info('程序退出...')
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
        # 位置判定 TODO

        return True

    @staticmethod
    def _cv2_add_chinese_text(img, text, position, text_color=(0, 255, 0), text_size=30):
        """
        给图片加中文文字

        :param img: 图片
        :param text: 文本
        :param position: 位置
        :param text_color: 文字颜色
        :param text_size: 文字大小
        :return: img 图片
        """
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

    def init_all_static_var(self):
        """
        初始化所有的参数
        使用情况：
            未识别到人脸
            检测到换人
        """
        self.face_search_lock = False
        self.person_id = None
        self.person_name = None
        self.is_temp = False

    def temp_compensation(self, obj_temp, outside_temp):
        """
        温度补偿

        测腕温 开启温度补偿
        开启温度&距离补偿：先补偿距离再转化温度

        :param obj_temp: 人体温度
        :param outside_temp: 室温
        :return:
        """
        if not obj_temp or not outside_temp:
            return False
        if sys_config.distance_compensation:  # 开启距离补偿
            obj_temp = TempComp.distance_compensation(obj_temp)
        person_temp = obj_temp
        if sys_config.measure_parts:  # 测腕温 开启温度补偿
            temp_comp = TempComp(obj_temp, outside_temp)
            person_temp = temp_comp.wrist_to_forehead_temp()
        return person_temp

    def data_save(self):
        person_name = self.person_name
        person_id = self.person_id
