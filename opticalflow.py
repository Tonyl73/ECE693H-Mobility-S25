import board
import busio
import digitalio
import time

# Define SPI pins using CircuitPython's board module
SCK_PIN = board.D8  # Serial clock
MOSI_PIN = board.D7  # Master Out Slave In
MISO_PIN = board.D6  # Master In Slave Out
CS_PIN = board.D5  # Chip Select (CS)
INT_PIN = board.D4  # Interrupt Pin

# Initialize SPI with the defined pins
spi = busio.SPI(SCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

# Set up the chip select (CS) pin
cs = digitalio.DigitalInOut(CS_PIN)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # Default HIGH (inactive)

# Set up the interrupt (INT) pin
int_pin = digitalio.DigitalInOut(INT_PIN)
int_pin.direction = digitalio.Direction.INPUT
int_pin.pull = digitalio.Pull.UP  # Set to pull-up to detect low signal when active

class PAA5100JE:
    def __init__(self, spi, cs, int_pin):
        self.spi = spi
        self.cs = cs
        self.int_pin = int_pin
        self.initialize_sensor()

    def write_register(self, reg, value):
        """Write a value to a register."""
        self.cs.value = False  # Select sensor
        if not self.spi.try_lock():  # Try to acquire SPI lock
            raise RuntimeError("SPI bus is busy")
        try:
            self.spi.write(bytearray([reg | 0x80, value]))  # MSB set for write
        finally:
            self.spi.unlock()  # Always unlock SPI bus after the transaction
        self.cs.value = True  # Deselect sensor
        time.sleep(0.00005)  # 50µs delay for the sensor to process

    def read_register(self, reg):
        """Read a value from a register."""
        self.cs.value = False  # Select sensor
        if not self.spi.try_lock():  # Try to acquire SPI lock
            raise RuntimeError("SPI bus is busy")
        try:
            self.spi.write(bytearray([reg & 0x7F]))  # Send register address (MSB set to 0)
            result = bytearray(1)
            self.spi.readinto(result)  # Read a byte into the result array
        finally:
            self.spi.unlock()  # Always unlock SPI bus after the transaction
        self.cs.value = True  # Deselect sensor
        return result[0]

    def initialize_sensor(self):
        """Initialize the sensor and check if it's detected."""
        prod_id = self.read_register(0x00)  # Read the Product ID register
        if prod_id == 0x49:
            print(" PAA5100JE detected!")
        else:
            print(f" Unexpected ID: {prod_id}")

    def get_motion(self):
        """Get motion data (delta X and delta Y)."""
        dx = self.read_register(0x03)  # Motion delta X
        dy = self.read_register(0x04)  # Motion delta Y
        return dx, dy

    def check_interrupt(self):
        """Check the INT pin for motion detection."""
        return not self.int_pin.value  # INT is active-low, so we check if it's low

# Initialize the sensor
sensor = PAA5100JE(spi, cs, int_pin)

# Main loop: Check for interrupts and print motion data when interrupt occurs
while True:
    if sensor.check_interrupt():  # Check if the INT pin was triggered
        dx, dy = sensor.get_motion()
        print(f"Delta X: {dx}, Delta Y: {dy}")
        time.sleep(0.1)
    else:
        time.sleep(0.01)  # Short delay to avoid busy-waiting

