import depthai
import math

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.kd = kd
        self.ki = ki
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, current_value):
        error = setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative


