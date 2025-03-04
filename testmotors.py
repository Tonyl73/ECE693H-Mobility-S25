import board
import pwmio
import digitalio
import time

# Define motor driver pins (Use appropriate GPIOs)
AIN1 = pwmio.PWMOut(board.A2, frequency=1000, duty_cycle=0)  # PWM for direction 1
AIN2 = pwmio.PWMOut(board.A1, frequency=1000, duty_cycle=0)  # PWM for direction 2

BIN1 = pwmio.PWMOut(board.A3, frequency=1000, duty_cycle=0)  # PWM for direction 1
BIN2 = pwmio.PWMOut(board.A4, frequency=1000, duty_cycle=0)  # PWM for direction 2

# STBY pin (if required by the motor driver)
# STBY = digitalio.DigitalInOut(board.D4)
# STBY.direction = digitalio.Direction.OUTPUT
# STBY.value = True  # Always enabled

def motor_forward1(speed):
    """Move motor 1 forward at a given speed (0-65535)."""
    AIN1.duty_cycle = speed
    AIN2.duty_cycle = 0

def motor_backward1(speed):
    """Move motor 1 backward at a given speed (0-65535)."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = speed

def motor_stop1():
    """Stop motor 1."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0

def motor_forward2(speed):
    """Move motor 2 forward at a given speed (0-65535)."""
    BIN1.duty_cycle = speed
    BIN2.duty_cycle = 0

def motor_backward2(speed):
    """Move motor 2 backward at a given speed (0-65535)."""
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = speed
    
def motor_stop2():
    """Stop motor 2."""
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = 0

# Example Usage
while True:
    motor_forward1(65535)  # Motor 1 forward
    motor_forward2(65535)  # Motor 2 forward
    time.sleep(1)
    
    motor_backward1(65535)  # Motor 1 backward
    motor_backward2(65535)  # Motor 2 backward
    time.sleep(1)
    
    motor_stop1()  # Stop motor 1
    motor_stop2()  # Stop motor 2
    time.sleep(2)
