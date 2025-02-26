# ECE693 Mobility Subsystem - Robotics Project

## Overview
Welcome to the **Mobility Subsystem** repository! This subsystem is responsible for designing and implementing the movement and localization capabilities of our robot. Our key objectives include motor and wheel selection, motor driver and encoder integration, power distribution, PID controller tuning, and top-down motion tracking.

## Responsibilities
As part of the Mobility team, our focus includes:
- **Wheels and Motors**: Selecting appropriate motors and gearing solutions.
- **Motor Driver Electronics**: Choosing and integrating motor drivers.
- **Encoder Electronics**: Handling motor encoders for precise control.
- **Power Distribution**: Ensuring appropriate power management for motors.
- **PID Controller Tuning**: Fine-tuning PID parameters for accurate motor speed (RPM) control.
- **Motion Capture**: Implementing a top-down tracking system using AprilTags or WhyCon.

## Tracking System
We will use a top-down tracking approach leveraging:
- [WhyCon](https://github.com/jiriUlr/whycon-ros)
- [AprilTags](https://github.com/christianrauch/apriltag_ros)
- A **cheap USB webcam** included in the kit

## Motor and Motor Driver Selection
- **Motors**: Considering TT motors with embedded encoders for simplicity ([Example TT Motor](https://www.hiwonder.com/products/tt-motor-plastic?variant=40452432298071&srsltid=AfmBOoqYtg5Yp8X2HhM_1UxTe5uOhzZg6eclLhZCLnoyyDC-aWa29SCf))
- **Motor Drivers**: Selecting appropriate drivers based on power and control needs
- **Power Analysis**:
  - Quiescent power draw
  - Average power consumption during motion
  - RPM/Torque power requirements
  - Voltage/current estimations

## Project Timeline
### Key Deadlines
- **February 3rd**: Order components for prototyping (breadboard level, breakout boards allowed)
- **Design Review 1**:
  - Motor and gearing selection methodology
  - Motor driver selection methodology
  - Power estimation and voltage/current requirements
  - Overview of tracking technique
  - Project timeline until **Design Review 2** (March 10th)
- **March 10th**: Design Review 2

## Hardware Assumptions
- **Microcontroller**: Instructor-supplied **Arduino Nano ESP32**
- **Budget**: ~$100 per robot (budget is not a concern, but cost-effectiveness is encouraged)
- **Miscellaneous Components**: Wires, breadboards, and passive components will be supplied

## Getting Started
1. Clone this repository:
   ```sh
   git clone https://github.com/YOUR_REPOSITORY_URL.git
   ```
2. Install necessary dependencies and libraries for motor control and tracking.
3. Prototype circuits using the Arduino Nano ESP32 and selected motor drivers.
4. Implement and test PID control for motor speed regulation.
5. Integrate and calibrate the top-down motion tracking system.

## Contribution Guidelines
- Use feature branches for development.
- Submit pull requests for code reviews.
- Document major changes in the `docs/` folder.
- Keep discussions and issues organized in the repository.

## Lead Software Engineers
-Byron 
-Matthew 


