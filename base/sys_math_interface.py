import math


class SysMath:
    @staticmethod
    def ptop_distance(x1, y1, x2, y2):
        """
        两点间的距离
        :param x1:
        :param y1:
        :param x2:
        :param y2:
        :return: distance
        """
        distance = math.sqrt(pow(x1 - x2, 2) * pow(y1 - y2, 2))
        return distance


math_server = SysMath()
