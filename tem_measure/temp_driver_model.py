import smbus
from time import sleep
from base.conf_obtain import sys_config
from tem_measure.temp_comp_model import TempComp


class MLX90614:
    OPEN_COMPENSTATE = sys_config.distance_compensation

    MLX90614_RAWIR1 = 0x04
    MLX90614_RAWIR2 = 0x05
    MLX90614_TA = 0x06
    MLX90614_TOBJ1 = 0x07
    MLX90614_TOBJ2 = 0x08

    MLX90614_TOMAX = 0x20
    MLX90614_TOMIN = 0x21
    MLX90614_PWMCTRL = 0x22
    MLX90614_TARANGE = 0x23
    MLX90614_EMISS = 0x24
    MLX90614_CONFIG = 0x25
    MLX90614_ADDR = 0x0E
    MLX90614_ID1 = 0x3C
    MLX90614_ID2 = 0x3D
    MLX90614_ID3 = 0x3E
    MLX90614_ID4 = 0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, address=0x5a, bus_num=1):
        self.bus_num = bus_num
        self.address = address
        self.bus = smbus.SMBus(bus=bus_num)

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                # "Rate limiting" - sleeping to prevent problems with sensor
                # when requesting data too quickly
                # sleep(self.comm_sleep_amount)
        # By this time, we made a couple requests and the sensor didn't respond
        # (judging by the fact we haven't returned from this function yet)
        # So let's just re-raise the last IOError we got
        raise err

    def data_to_temp(self, data):
        temp = (data * 0.02) - 273.15
        return temp

    def get_outside_temp(self):
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)

    def get_temp(self):
        temp_list = []
        count = 0
        while len(temp_list) < 6:
            if count > 20:
                break
            count += 1
            obj_temp = self.get_obj_temp()
            outside_temp = self.get_outside_temp()
            if self.OPEN_COMPENSTATE:
                temp_comp_obj = TempComp(obj_temp=obj_temp, outside_temp=outside_temp)
                act_temp = temp_comp_obj.wrist_to_forehead_temp()
            else:
                act_temp = obj_temp
            if act_temp:
                temp_list.append(act_temp)
            count += 1
        if not temp_list:
            return None
        temp_list = sorted(temp_list)

        return temp_list[int(len(temp_list) / 2)]


enable_temp_driver = MLX90614()

if __name__ == "__main__":

    while 1:
        temp = enable_temp_driver.get_temp()
        if temp:
            print(temp)
        else:
            print('----')

    # print(temp_comp_obj.forehead_temp)
