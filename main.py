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

def M1F(speed):
    """Move motor 1 forward at a given speed (0-65535)."""
    AIN1.duty_cycle = speed
    AIN2.duty_cycle = 0

def M1B(speed):
    """Move motor 1 backward at a given speed (0-65535)."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = speed

def M1S():
    """Stop motor 1."""
    AIN1.duty_cycle = 0
    AIN2.duty_cycle = 0

def M2F(speed):
    """Move motor 2 forward at a given speed (0-65535)."""
    BIN1.duty_cycle = speed
    BIN2.duty_cycle = 0

def M2B(speed):
    """Move motor 2 backward at a given speed (0-65535)."""
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = speed

def M2S():
    """Stop motor 2."""
    BIN1.duty_cycle = 0
    BIN2.duty_cycle = 0

def M3F(speed):
    """Move motor 2 forward at a given speed (0-65535)."""
    CIN1.duty_cycle = speed
    CIN2.duty_cycle = 0

def M3B(speed):
    """Move motor 2 backward at a given speed (0-65535)."""
    CIN1.duty_cycle = 0
    CIN2.duty_cycle = speed

def M3S():
    """Stop motor 2."""
    CIN1.duty_cycle = 0
    CIN2.duty_cycle = 0


def all_stop():
    M1S()
    M2S()
    M3S()

def move_F1(speed):
    """Moves robot straight forward on 1."""
    M3F(speed)  
    M2F(speed)  
   
def move_F2(speed):
    M3B(speed)
    M1F(speed)

def move_F3(speed):
    M1B(speed)
    M2B(speed)

def move_B1(speed):
    M3B(speed)
    M2B(speed)

def move_B2(speed):
    M3F(speed)
    M1B(speed)

def move_B3(speed):
    M1F(speed)
    M2F(speed)

def circle_cw(speed):
    M1B(speed)
    M3B(speed)
    M2F(speed)

def circle_ccw(speed):
    M1F(speed)
    M3F(speed)
    M2B(speed)


#Testing linear and rotational motion
#while True:
    s = 65535
    time.sleep(5)
    move_F1(s)
    time.sleep(7)
    all_stop()
    move_B1(s)
    time.sleep(7)
    all_stop()
    move_F2(s)
    time.sleep(7)
    all_stop()
    move_B2(s)
    time.sleep(7)
    all_stop()
    move_F3(s)
    time.sleep(7)
    all_stop()
    move_B3(s)
    time.sleep(7)
    all_stop()
    circle_cw(s)
    time.sleep(7)
    all_stop()
    circle_ccw(s)
    time.sleep(7)
    all_stop()

#Testing omni-motion
#while True:



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


# Move in a circle
#while True:
    for angle in range(0, 360, 10):  # 10° increments

        rad = math.radians(angle)
        Vx = math.cos(rad) * 50000
        Vy = math.sin(rad) * 50000
        S1, S2, S3 = compute_motor_speeds(Vx, Vy)


    # Apply speeds to motors
        M1F(S1)
        M2F(S2)
        M3F(S3)

        time.sleep(0.1)  # Small delay for smooth motion



    '''
def move_right(speed):
    """Moves robot to the right (strafe)."""
    M1S()  # Front wheel doesn’t contribute
    M2B(int(speed * 0.866))  # Rear-left moves
    M3F(int(speed * 0.866))  # Rear-right moves

def move_diagonal(speed):
    """Moves robot diagonally forward-right."""
    M1F(speed)  # Full speed
    M2B(int(speed * 0.5 + speed * 0.866))  # Adjusted for angle
    M3F(int(speed * 0.5 - speed * 0.866))  # Adjusted for angle

#while True:
    move_circle(30000)  # Circle rotation
    time.sleep(5)
    
    move_forward(40000)  # Forward
    time.sleep(3)

    move_right(40000)  # Right
    time.sleep(3)

    move_diagonal(40000)  # Diagonal
    time.sleep(3)

    M1S()
    M2S()
    M3S()
    time.sleep(2)
    '''
