#include <SPI.h>
#include "Bitcraze_PMW3901.h"
// Change the pin below if your CS pin is different.
#define FLOW_CS_PIN 10

// Create a Bitcraze_PMW3901 instance.
Bitcraze_PMW3901 flowSensor(FLOW_CS_PIN);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    // Wait for serial port to be available (needed on some boards like the Leonardo)
  }

  // Start up the sensor
  if (!flowSensor.begin()) {
    Serial.println("Failed to detect or initialize the PMW3901 sensor!");
    while (1) {
      // If we fail to detect the sensor, stay here forever.
    }
  }
  Serial.println("PMW3901 optical flow sensor initialized successfully!");

  // Optionally, turn the sensor LED on or off:
  flowSensor.setLed(true);  // Turn LED on
  flowSensor.setLed(false); // Turn LED off
}

void loop() {
  // Variables to hold the motion data
  int16_t deltaX, deltaY;

  // Read current motion counts
  flowSensor.readMotionCount(&deltaX, &deltaY);

  Serial.print("Delta X: ");
  Serial.print(deltaX);
  Serial.print(" | Delta Y: ");
  Serial.println(deltaY);

  // Small delay to avoid spamming the serial output too quickly
  delay(100);
}
