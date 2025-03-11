import board
import pwmio
import digitalio
import time
import math

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


#### Motor Control ####


# Define motor driver pins (Use appropriate GPIOs)
AIN1 = pwmio.PWMOut(board.A2, frequency=1000, duty_cycle=0)  # PWM for direction 1
AIN2 = pwmio.PWMOut(board.A1, frequency=1000, duty_cycle=0)  # PWM for direction 2

BIN1 = pwmio.PWMOut(board.A3, frequency=1000, duty_cycle=0)  # PWM for direction 1
BIN2 = pwmio.PWMOut(board.A4, frequency=1000, duty_cycle=0)  # PWM for direction 2

CIN1 = pwmio.PWMOut(board.A5, frequency=1000, duty_cycle=0)  # PWM for direction 1
CIN2 = pwmio.PWMOut(board.A6, frequency=1000, duty_cycle=0)  # PWM for direction 2
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

def motor_forward3(speed):
    """Move motor 2 forward at a given speed (0-65535)."""
    CIN1.duty_cycle = speed
    CIN2.duty_cycle = 0

def motor_backward3(speed):
    """Move motor 2 backward at a given speed (0-65535)."""
    CIN1.duty_cycle = 0
    CIN2.duty_cycle = speed

def motor_stop3():
    """Stop motor 2."""
    CIN1.duty_cycle = 0
    CIN2.duty_cycle = 0

def compute_motor_speeds(Vx, Vy, max_pwm=65535):
    """Compute the speed for each omniwheel given a desired velocity vector (Vx, Vy)."""
    
    # Calculate motor speed contributions
    S1 = Vx
    S2 = (-0.5 * Vx) + ((math.sqrt(3) / 2) * Vy)
    S3 = (-0.5 * Vx) - ((math.sqrt(3) / 2) * Vy)

    # Normalize speeds if they exceed max PWM
    max_speed = max(abs(S1), abs(S2), abs(S3))
    if max_speed > max_pwm:
        S1 = int(S1 * (max_pwm / max_speed))
        S2 = int(S2 * (max_pwm / max_speed))
        S3 = int(S3 * (max_pwm / max_speed))
    
    return int(S1), int(S2), int(S3)

#Example Usage
while True:
    time.sleep(5)
    motor_forward1(65535)  # Motor 1 forward
    motor_backward2(65535)  # Motor 2 forward
    motor_forward3(65535)
    time.sleep(5)
    motor_stop1()
    time.sleep(5)
    motor_forward1(65535)
    time.sleep(5) 
    motor_stop2()
    time.sleep(5)
    motor_backward2(65535)
    time.sleep(5)
    motor_stop3()
    time.sleep(5)



# Move in a circle
for angle in range(0, 360, 10):  # 10° increments

    rad = math.radians(angle)
    Vx = math.cos(rad) * 50000
    Vy = math.sin(rad) * 50000
    S1, S2, S3 = compute_motor_speeds(Vx, Vy)


    # Apply speeds to motors
    motor_forward1(S1)
    motor_forward2(S2)
    motor_forward3(S3)

    time.sleep(0.1)  # Small delay for smooth motion






'''
def move_circle(speed):
    """Moves the robot in a circular motion (pure rotation)."""
    motor_forward1(speed)
    motor_backward2(speed)
    motor_forward3(speed)


def move_forward(speed):
    """Moves robot straight forward."""
    motor_forward1(speed)  # Front wheel full forward
    motor_backward2(speed // 2)  # Rear-left half speed backward
    motor_backward3(speed // 2)  # Rear-right half speed backward

def move_right(speed):
    """Moves robot to the right (strafe)."""
    motor_stop1()  # Front wheel doesn’t contribute
    motor_backward2(int(speed * 0.866))  # Rear-left moves
    motor_forward3(int(speed * 0.866))  # Rear-right moves

def move_diagonal(speed):
    """Moves robot diagonally forward-right."""
    motor_forward1(speed)  # Full speed
    motor_backward2(int(speed * 0.5 + speed * 0.866))  # Adjusted for angle
    motor_forward3(int(speed * 0.5 - speed * 0.866))  # Adjusted for angle

while True:
    move_circle(30000)  # Circle rotation
    time.sleep(5)
    
    move_forward(40000)  # Forward
    time.sleep(3)

    move_right(40000)  # Right
    time.sleep(3)

    move_diagonal(40000)  # Diagonal
    time.sleep(3)

    motor_stop1()
    motor_stop2()
    motor_stop3()
    time.sleep(2)


'''
