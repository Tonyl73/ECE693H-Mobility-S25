import board
import digitalio
import pwmio
import time
import rotaryio

# Define encoder pins
encoder_left = rotaryio.IncrementalEncoder(board.A1, board.A2)
encoder_right = rotaryio.IncrementalEncoder(board.D5, board.D6)

# Motor control pins
motor1_pwm = pwmio.PWMOut(board.A4, duty_cycle=0)  # M1 PWM Pin
motor2_pwm = pwmio.PWMOut(board.D4, duty_cycle=0)  # M2 PWM Pin
motor1_dir = digitalio.DigitalInOut(board.A3)
motor1_dir.direction = digitalio.Direction.OUTPUT
motor2_dir = digitalio.DigitalInOut(board.D3)
motor2_dir.direction = digitalio.Direction.OUTPUT

# PID constants
Kp_left, Ki_left, Kd_left = 1.0, 0.0, 0.5
Kp_right, Ki_right, Kd_right = 1.0, 0.0, 0.5
base_speed = 25  # Base RPM

# Sensor pins and thresholds
sensor_pins = [board.D10, board.D9, board.D8, board.A5, board.A6, board.A7]
white_val, black_val = 1000, 2000

# Sensor setup
ctrl_even = digitalio.DigitalInOut(board.D12)
ctrl_even.direction = digitalio.Direction.OUTPUT
sensors = [digitalio.DigitalInOut(pin) for pin in sensor_pins]
for sensor in sensors:
    sensor.direction = digitalio.Direction.OUTPUT
    sensor.value = True

# Helper functions
def map_rpm_to_duty_cycle(rpm, min_rpm, max_rpm, min_duty=0, max_duty=65535):
    rpm = max(min_rpm, min(max_rpm, rpm))
    return int((rpm - min_rpm) / (max_rpm - min_rpm) * (max_duty - min_duty) + min_duty)

def calculate_rpm(encoder, last_position, delta_time):
    delta_position = encoder.position - last_position
    return (delta_position / 1440) * (60 / delta_time), encoder.position

def normalize_sensor_values(sensor_values):
    return [max(0.0, min(1.0, (val - white_val) / (black_val - white_val))) for val in sensor_values]

def compute_error(sensor_values):
    weights = [-3, -2, -1, 1, 2, 3]
    normalized_values = normalize_sensor_values(sensor_values)
    error = sum(weight * value for weight, value in zip(weights, normalized_values))
    return error, all(value >= 0.7 for value in normalized_values), all(value <= 0.3 for value in normalized_values)

def pid_motor_control(target_rpm, current_rpm, last_error, integral, Kp, Ki, Kd, motor_pwm, motor_dir):
    error = target_rpm - current_rpm
    integral += error
    derivative = error - last_error
    correction = Kp * error + Ki * integral + Kd * derivative
    duty_cycle = map_rpm_to_duty_cycle(correction, -base_speed, base_speed)
    motor_pwm.duty_cycle = abs(duty_cycle)
    motor_dir.value = correction < 0
    return error, integral

def read_sensors():
    ctrl_even.value = True
    for sensor in sensors:
        sensor.switch_to_output(value=True)
    time.sleep(0.00002)
    for sensor in sensors:
        sensor.switch_to_input(pull=None)
    start_time = time.monotonic_ns()
    decay_times = [0] * len(sensors)
    while not all(decay_times):
        for i, sensor in enumerate(sensors):
            if not decay_times[i] and not sensor.value:
                decay_times[i] = time.monotonic_ns() - start_time
    ctrl_even.value = False
    return [time_ns / 1000 for time_ns in decay_times]

# Line-following logic
def pid_line_following():
    global base_speed
    sensor_values = read_sensors()
    error, all_black, all_white = compute_error(sensor_values)

    if all_white:
        motor1_pwm.duty_cycle = motor2_pwm.duty_cycle = 0
        return

    delta_time = 0.05
    current_left_rpm, _ = calculate_rpm(encoder_left, 0, delta_time)
    current_right_rpm, _ = calculate_rpm(encoder_right, 0, delta_time)

    last_error_left, integral_left = pid_motor_control(
        base_speed + error, current_left_rpm, 0, 0,
        Kp_left, Ki_left, Kd_left, motor1_pwm, motor1_dir
    )
    last_error_right, integral_right = pid_motor_control(
        base_speed - error, current_right_rpm, 0, 0,
        Kp_right, Ki_right, Kd_right, motor2_pwm, motor2_dir
    )

# Main loop
while True:
    pid_line_following()
    time.sleep(0.05)

