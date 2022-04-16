import math

from distance_measure.distance_driver_model import enable_distance_driver


class TempComp:
    def __init__(self, obj_temp, outside_temp=None):
        self.obj_temp = obj_temp
        self.outside_temp = outside_temp

    def wrist_to_forehead_temp(self):
        """腕温--->额温  补偿"""
        wrist_temp = self.obj_temp
        outside_temp = self.outside_temp
        # self._distance_comp(wrist_temp, distance=3)  # 可以不考虑距离补偿
        wrist_temp_2 = math.pow(wrist_temp, 2)
        wrist_temp_3 = math.pow(wrist_temp, 3)
        forehead_temp = 0.02411 * wrist_temp_3 - 2.288 * wrist_temp_2 - 0.004356 * wrist_temp_2 * outside_temp + 0.2851 * wrist_temp * outside_temp - 4.702 * outside_temp + 72.46 * wrist_temp - 728.9 + 1.6
        if 36 < forehead_temp < 38:
            return forehead_temp
        return None

    @staticmethod
    def distance_compensation(temp):
        """距离补偿"""
        distance = enable_distance_driver.get_distance()
        temp = 0.5179 * distance + 0.9436 * distance - 0.0139 * distance * temp + 2.1898
        return temp
