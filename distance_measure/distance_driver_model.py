import RPi.GPIO as GPIO
import time


class DistanceDriver:
    TRIG = 24
    ECHO = 23
    RED_LED = 26
    pwm = None
    INTERVAL = 5

    def distanceInit(self):
        """使能GPIO串口"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def distanceStart(self):
        """测距"""
        # 发送trig信号，持续10us的方波脉冲
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)

        # 等待低电平结束，然后记录时间
        while GPIO.input(self.ECHO) == 0:
            pass
        pulse_start = time.time()

        # 等待高电平结束，然后记录时间
        while GPIO.input(self.ECHO) == 1:
            pass
        pulse_end = time.time()

        # 距离(单位:m)  =  (pulse_end – pulse_start) * 声波速度 / 2
        # 声波速度取 343m/s
        #
        # 距离(单位:cm) = (pulse_end – pulse_start) * 声波速度 / 2 * 100
        # 即 (pulse_end – pulse_start) * 17150
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        # print("Distance:{}cm".format(distance))
        return distance

    def ledStart(self):
        """LED闪烁"""
        GPIO.setup(self.RED_LED, GPIO.OUT)
        # 创建一个 PWM 实例，需要两个参数，第一个是GPIO端口号，这里用26号
        # 第二个是频率（Hz），频率越高LED看上去越不会闪烁，相应对CPU要求就越高，设置合适的值就可以
        self.pwm = GPIO.PWM(self.RED_LED, 60)

        # 启用PWM，参数是占空比，范围：0.0<=占空比<=100.0
        self.pwm.start(0)
        for i in range(3):
            # 电流从小到大，LED由暗到亮
            for i in range(101):
                # 更改占空比
                self.pwm.ChangeDutyCycle(i)
                time.sleep(0.02)

            # 电流从大到小，LED由亮变暗
            for i in range(100, -1, -1):
                self.pwm.ChangeDutyCycle(i)
                time.sleep(0.02)
        self.pwm.stop()

    def get_distance(self):
        try:
            self.distanceInit()
            distance = self.distanceStart()
            return distance
        except KeyboardInterrupt:
            if self.pwm is not None:
                self.pwm.stop()
            GPIO.cleanup()


enable_distance_driver = DistanceDriver()

if __name__ == '__main__':
    while True:
        disce_list = []
        for i in range(5):
            disce_list.append(enable_distance_driver.get_distance())
        disce_list.sort()
        disce_list.remove(disce_list[0])
        disce_list.remove(disce_list[-1])
        res = 0
        for i in disce_list:
            res += i
        res = res / len(disce_list)
        print('res:', res)
        time.sleep(2)
