#include <Arduino.h>
#include <SPI.h>
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <geometry_msgs/msg/Twist.h>
#include <sensor_msgs/msg/laser_scan.h>
#include <sensor_msgs/msg/battery_state.h>
#include <geometry_msgs/msg/pose_stamped.h>
#include <rosidl_runtime_c/string_functions.h>

// === Robot Configuration ===
#define ROBOT_NAMESPACE "/robot2"

// === Feature Flags ===
#define SERIAL_OUTPUT 1
#define SUB_VEL 1
#define PUB_SCAN 0
#define PUB_BAT 0
#define SUB_POSE 0
#define PUB_OPTICAL_FLOW 1

// === Communication Mode ===
#define MODE "WIFI"
#define AGENT_IP "192.168.4.1"
#define SSID "DRL_ROSPI"
#define NETPASS "369369369"

// === Hardware Configuration ===
#define LED_PIN 13

#define MOTOR1_PWM D5
#define MOTOR2_PWM D3
#define MOTOR3_PWM D4

#define MOTOR1_IN1 A1
#define MOTOR1_IN2 A2
#define MOTOR2_IN1 A3
#define MOTOR2_IN2 A4
#define MOTOR3_IN1 A5
#define MOTOR3_IN2 A6

#define LIDAR_NUM_POINTS 360
#define MAX_WHEEL_SPEED 1.0
#define PWM_MIN 15

// === SPI and Optical Flow Pins ===
#define CS_PIN D5   // Chip Select
#define INT_PIN D4  // Interrupt from sensor

// === ROS 2 Core ===
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

// === Motor Control ===
rcl_subscription_t sub_cmd_vel;
geometry_msgs__msg__Twist msg_cmd_vel;

// === Optical Flow Data ===
int16_t dx_total = 0;
int16_t dy_total = 0;

// === Error Handling Macros ===
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){error_loop();} }
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){} }

// === Utility ===
void error_loop() {
    while (1) {
        digitalWrite(LED_PIN, !digitalRead(LED_PIN));
        delay(100);
    }
}

int velocityToPWM(float wheel_velocity) {
    if (abs(wheel_velocity) < 0.01) return 0;
    float speed_ratio = abs(wheel_velocity) / MAX_WHEEL_SPEED;
    return constrain(PWM_MIN + speed_ratio * (255 - PWM_MIN), 0, 255);
}

// === ROS 2 Callback ===
void cmdVelCallback(const void *msg_in) {
    const geometry_msgs__msg__Twist *msg = (const geometry_msgs__msg__Twist *)msg_in;
    float Vx = msg->linear.x, Vy = msg->linear.y, omega = msg->angular.z;
    float V1 = Vx + omega * 0.15;
    float V2 = -0.5 * Vx + 0.866 * Vy + omega * 0.15;
    float V3 = -0.5 * Vx - 0.866 * Vy + omega * 0.15;

    digitalWrite(MOTOR1_IN1, V1 > 0);
    digitalWrite(MOTOR1_IN2, V1 < 0);
    analogWrite(MOTOR1_PWM, velocityToPWM(V1));

    digitalWrite(MOTOR2_IN1, V2 > 0);
    digitalWrite(MOTOR2_IN2, V2 < 0);
    analogWrite(MOTOR2_PWM, velocityToPWM(V2));

    digitalWrite(MOTOR3_IN1, V3 > 0);
    digitalWrite(MOTOR3_IN2, V3 < 0);
    analogWrite(MOTOR3_PWM, velocityToPWM(V3));

    Serial.printf("PWM: (%d, %d, %d)\n", velocityToPWM(V1), velocityToPWM(V2), velocityToPWM(V3));
}

// === Optical Flow Sensor Class ===
class PAA5100JE {
public:
    PAA5100JE(uint8_t cs_pin, uint8_t int_pin) : cs_pin(cs_pin), int_pin(int_pin) {}

    void begin() {
        pinMode(cs_pin, OUTPUT);
        digitalWrite(cs_pin, HIGH);

        pinMode(int_pin, INPUT_PULLUP);

        SPI.begin();

        // Check product ID
        uint8_t id = readRegister(0x00);
        if (id != 0x49) {
            Serial.print("PAA5100JE not found, ID: ");
            Serial.println(id, HEX);
        } else {
            Serial.println("PAA5100JE detected");
        }
    }

    bool hasMotion() {
        return digitalRead(int_pin) == LOW;
    }

    void readMotion(int16_t &dx, int16_t &dy) {
        dx = (int8_t)readRegister(0x03);
        dy = (int8_t)readRegister(0x04);
    }

private:
    uint8_t cs_pin, int_pin;

    uint8_t readRegister(uint8_t reg) {
        digitalWrite(cs_pin, LOW);
        SPI.beginTransaction(SPISettings(2000000, MSBFIRST, SPI_MODE3));
        SPI.transfer(reg & 0x7F);
        uint8_t value = SPI.transfer(0);
        SPI.endTransaction();
        digitalWrite(cs_pin, HIGH);
        delayMicroseconds(50);
        return value;
    }
};

// === Sensor Instance ===
PAA5100JE opticalSensor(CS_PIN, INT_PIN);

// === Setup ===
void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);

    if (MODE == "SERIAL") set_microros_transports();
    else if (MODE == "WIFI") set_microros_wifi_transports(SSID, NETPASS, AGENT_IP, 8888);

    for (int pin : {MOTOR1_IN1, MOTOR1_IN2, MOTOR2_IN1, MOTOR2_IN2, MOTOR3_IN1, MOTOR3_IN2, MOTOR1_PWM, MOTOR2_PWM, MOTOR3_PWM}) {
        pinMode(pin, OUTPUT);
    }

    // Initialize ROS 2
    allocator = rcl_get_default_allocator();
    rclc_support_init(&support, 0, NULL, &allocator);
    RCCHECK(rclc_node_init_default(&node, "robot_node", "", &support));
    RCCHECK(rclc_executor_init(&executor, &support.context, 1, &allocator));

    if (SUB_VEL) {
        char topic[50];
        snprintf(topic, sizeof(topic), "%s/cmd_vel", ROBOT_NAMESPACE);
        RCCHECK(rclc_subscription_init_default(&sub_cmd_vel, &node, ROSIDL_GET_MSG_TYPE_SUPPORT(geometry_msgs, msg, Twist), topic));
        RCCHECK(rclc_executor_add_subscription(&executor, &sub_cmd_vel, &msg_cmd_vel, &cmdVelCallback, ON_NEW_DATA));
    }

    // Initialize optical flow sensor
    opticalSensor.begin();
}

// === Main Loop ===
void loop() {
    RCSOFTCHECK(rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100)));

    // Read motion if INT pin triggered
    if (opticalSensor.hasMotion()) {
        int16_t dx, dy;
        opticalSensor.readMotion(dx, dy);
        dx_total += dx;
        dy_total += dy;
        Serial.printf("Δx: %d, Δy: %d (Total: %d, %d)\n", dx, dy, dx_total, dy_total);
        delay(50);
    }

    delay(10);
}
