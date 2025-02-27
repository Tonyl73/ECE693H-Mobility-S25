import board
import time
import pwmio
import digitalio

AIN1 = digitalio.DigitalInOut(board.A1)
AIN1.direction = digitalio.Direction.OUTPUT

AIN2 = digitalio.DigitalInOut(board.A2)
AIN2.direction = digitalio.Direction.OUTPUT

pwm = pwmio.PWMOut(board.D6, duty_cycle=0, frequency=1000)
isStarted = False

def setMotor(motorNum, dutyCycle):
    minDC = 15  # Minimum duty cycle threshold
    kickstartDC = 100

    if motorNum == 'A':
        if dutyCycle > 0:
            AIN1.value = True
            AIN2.value = False
        elif dutyCycle < 0:
            AIN1.value = False
            AIN2.value = True
        else:
            AIN1.value = False
            AIN2.value = False
            pwm.duty_cycle = 0
            return

        # Kickstart logic to ensure the motor starts moving
        if abs(dutyCycle) < minDC:
            print("Applying kickstart")
            pwm.duty_cycle = int(kickstartDC / 100 * 65535)
            time.sleep(0.05)  # Give it a brief push

        # Set the actual PWM duty cycle
        dc = int(abs(dutyCycle) / 100 * 65535)
        print(f"Duty Cycle {dc}")
        pwm.duty_cycle = int(abs(dutyCycle) / 100 * 65535)

def map_value(input, inMin=0, inMax=63000, outMin=-100, outMax=100):
    return (input - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

def main():
    while True:
        dutyCycle = 100  # Example fixed duty cycle value
        #print(f"Duty Cycle {dutyCycle}")
        setMotor('A', dutyCycle)
        time.sleep(1)
        dutyCycle = -100
        setMotor('A', dutyCycle)
        time.sleep(1)
        
if __name__ == "__main__":
    
    main()
