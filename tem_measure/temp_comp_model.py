import math


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
        forehead_temp = 0.02411 * wrist_temp_3 - 2.288 * wrist_temp_2 - 0.004356 * wrist_temp_2 * outside_temp + 0.2851 * wrist_temp * outside_temp - 4.702 * outside_temp + 72.46 * wrist_temp - 728.9
        return forehead_temp

    def forehead_to_wrist_temp(self):
        """
        弃用!!!

        额温--->腕温  补偿
        由腕温--->额温补偿公式推导
        """
        # forehead_temp = self.forehead_temp
        # outside_temp = self.outside_temp

    @staticmethod
    def distance_compensation(temp, distance=20):
        """距离补偿"""
        temp = 0.5179 * distance + 0.9436 * distance - 0.0139 * distance * temp + 2.1898
        return temp

# if __name__ == '__main__':
#     obj = TempComp(wrist_temp=30, outside_temp=24)
#     print(obj.forehead_temp)
#     obj2 = TempComp(forehead_temp=obj.forehead_temp, outside_temp=24)
#     print(obj2.wrist_temp)
