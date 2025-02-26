import board
import pwmio
import digitalio
import time

Define motor driver pins (Use appropriate GPIOs)
AIN1 = pwmio.PWMOut(board.A0, frequency=1000, duty_cycle=0)  # PWM for direction 1
AIN2 = pwmio.PWMOut(board.A1, frequency=1000, duty_cycle=0)  # PWM for direction 2
STBY = digitalio.DigitalInOut(board.D4)  # Standby pin
STBY.direction = digitalio.Direction.OUTPUT
STBY.value = True  # Always keep enabled

def motor_forward(speed):
    """Move motor forward at a given speed (0-65535)."""
    AIN1.duty_cycle = speed
    AIN2.duty_cycle = 0

def motor_backward(speed):
    """Move motor backward at a given speed (0-65535)."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = speed

def motor_stop():
    """Stop the motor."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0

Example Usage
while True:
    motor_forward(50000)  # Run forward at ~75% speed
    time.sleep(2)
    motor_backward(50000)  # Run backward at ~75% speed
    time.sleep(2)
    motor_stop()  # Stop motor
    time.sleep(2)
