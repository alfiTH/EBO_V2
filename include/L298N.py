from dataclasses import dataclass
import time

from RPi import GPIO

@dataclass
class L298N:
    ENA: int
    IN1: int
    IN2: int
    IN3: int
    IN4: int
    ENB: int
    frecuency: int = 100
    mode_gpio: int = GPIO.BCM

    def __post_init__(self):

        try:
            channels = [self.ENA, self.IN1, self.IN2, self.IN3, self.IN4, self.ENB]

            GPIO.setmode(self.mode_gpio)
            GPIO.setup(channels, GPIO.OUT, initial=GPIO.LOW)

            self.PWMleft = GPIO.PWM(self.ENA, self.frecuency)
            self.PWMleft.start(0)
            self.PWMright = GPIO.PWM(self.ENB, self.frecuency)
            self.PWMright.start(0)

            self.motorEnable = False

        except Exception as e:
            print(f"Initialisation error, you may need to run the command sudo chmod 666 /dev/gpio*. \n\n{e}")
            raise

    def __del__(self):
        self.PWMright.stop()
        self.PWMleft.stop()
        GPIO.cleanup([self.ENA, self.IN1, self.IN2, self.IN3, self.IN4, self.ENB])

    def setStateMotor(self, state):
            self.motorEnable = state
            if not self.motorEnable:
                self.PWMleft.ChangeDutyCycle(0)
                self.PWMright.ChangeDutyCycle(0)

    def getStateMotor(self):
        return self.motorEnable

    def _setSpeed(self, speed:float, in1:int, in2:int, pwm:GPIO.PWM):
        if speed is not None:
            if speed < 0:
                speed = max(speed, -100)
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.HIGH)
                pwm.ChangeDutyCycle(abs(speed))
            elif speed > 0:
                speed = min(speed, 100) 
                GPIO.output(in1, GPIO.HIGH)
                GPIO.output(in2, GPIO.LOW)
                pwm.ChangeDutyCycle(speed)
            else:
                GPIO.output(in1, GPIO.LOW)
                GPIO.output(in2, GPIO.LOW)
                pwm.ChangeDutyCycle(0)

    def setSpeed(self, left_speed=None, right_speed=None):
        if self.motorEnable:
            self._setSpeed(left_speed, self.IN1, self.IN2, self.PWMleft)
            self._setSpeed(right_speed, self.IN3, self.IN4, self.PWMright)
