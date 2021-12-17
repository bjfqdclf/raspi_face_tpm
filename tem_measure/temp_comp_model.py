import math

class TempComp:
    def __init__(self, wrist_temp=None, forehead_temp=None, outside_temp=None):
        self.wrist_temp = wrist_temp
        self.forehead_temp =forehead_temp
        self.outside_temp = outside_temp
        # self.distance_comp()
        self.wrist_to_forehead_temp()

    def distance_comp(self):
        """距离补偿"""
        pass

    def wrist_to_forehead_temp(self):
        """腕温--->额温  补偿"""
        wrist_temp = self.wrist_temp
        outside_temp = self.outside_temp
        wrist_temp_2 = math.pow(wrist_temp, 2)
        wrist_temp_3 = math.pow(wrist_temp, 3)
        self.forehead_temp = 0.02411*wrist_temp_3-2.288*wrist_temp_2-0.004356*wrist_temp_2*outside_temp+0.2851*wrist_temp*outside_temp-4.702*outside_temp+72.46*wrist_temp-728.9

    def forehead_to_wrist_temp(self):
        """额温--->腕温  补偿"""
        pass

