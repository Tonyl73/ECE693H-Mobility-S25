import board
import pwmio
import digitalio
import time

# Define motor driver pins (using appropriate GPIOs)
PWMA = pwmio.PWMOut(board.D2, frequency=1000, duty_cycle=0)  # Motor A PWM
PWMB = pwmio.PWMOut(board.D3, frequency=1000, duty_cycle=0)  # Motor B PWM

AIN1 = digitalio.DigitalInOut(board.A1)  # Motor A direction
AIN2 = digitalio.DigitalInOut(board.A2)  
BIN1 = digitalio.DigitalInOut(board.A3)  # Motor B direction
BIN2 = digitalio.DigitalInOut(board.A4)  

STBY = digitalio.DigitalInOut(board.D4)  # Standby pin

# Set pin directions
AIN1.direction = digitalio.Direction.OUTPUT
AIN2.direction = digitalio.Direction.OUTPUT
BIN1.direction = digitalio.Direction.OUTPUT
BIN2.direction = digitalio.Direction.OUTPUT
STBY.direction = digitalio.Direction.OUTPUT

# Enable the motor driver
STBY.value = True  

def motorA_forward(speed):
    """Move Motor A forward at a given speed (0-65535)."""
    AIN1.value = True
    AIN2.value = False
    PWMA.duty_cycle = speed

def motorA_backward(speed):
    """Move Motor A backward at a given speed (0-65535)."""
    AIN1.value = False
    AIN2.value = True
    PWMA.duty_cycle = speed

def motorB_forward(speed):
    """Move Motor B forward at a given speed (0-65535)."""
    BIN1.value = True
    BIN2.value = False
    PWMB.duty_cycle = speed

def motorB_backward(speed):
    """Move Motor B backward at a given speed (0-65535)."""
    BIN1.value = False
    BIN2.value = True
    PWMB.duty_cycle = speed

def motor_stop():
    """Stop both motors."""
    AIN1.value = False
    AIN2.value = False
    BIN1.value = False
    BIN2.value = False
    PWMA.duty_cycle = 0
    PWMB.duty_cycle = 0

# Example Usage
while True:
    motorA_forward(50000)  # Motor A forward at ~75% speed
    motorB_forward(50000)  # Motor B forward at ~75% speed
    time.sleep(2)
    
    motorA_backward(50000)  # Motor A backward at ~75% speed
    motorB_backward(50000)  # Motor B backward at ~75% speed
    time.sleep(2)
    
    motor_stop()  # Stop motors
    time.sleep(2)
