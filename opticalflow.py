import board
import busio
import digitalio
import time

# Define SPI pins using CircuitPython's board module
SCK_PIN = board.SCK  # Serial clock
MOSI_PIN = board.MOSI  # Master Out Slave In
MISO_PIN = board.MISO  # Master In Slave Out
CS_PIN = board.D5  # Chip Select (CS)

# Initialize SPI with the defined pins
spi = busio.SPI(SCK_PIN, MOSI=MOSI_PIN, MISO=MISO_PIN)

# Set up the chip select (CS) pin
cs = digitalio.DigitalInOut(CS_PIN)
cs.direction = digitalio.Direction.OUTPUT
cs.value = True  # Default HIGH (inactive)

class PAA5100JE:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.initialize_sensor()

    def write_register(self, reg, value):
        """Write a value to a register."""
        self.cs.value = False  # Select sensor
        with self.spi as spi_lock:  # Lock SPI bus
            self.spi.write(bytearray([reg | 0x80, value]))  # Write with the MSB set to 1
        self.cs.value = True  # Deselect sensor
        time.sleep(0.00005)  # 50µs delay for the sensor to process

    def read_register(self, reg):
        """Read a value from a register."""
        self.cs.value = False  # Select sensor
        with self.spi as spi_lock:  # Lock SPI bus
            self.spi.write(bytearray([reg & 0x7F]))  # Send register address (MSB set to 0)
            result = bytearray(1)
            self.spi.readinto(result)  # Read a byte into the result array
        self.cs.value = True  # Deselect sensor
        return result[0]

    def initialize_sensor(self):
        """Initialize the sensor and check if it's detected."""
        prod_id = self.read_register(0x00)  # Read the Product ID register
        if prod_id == 0x49:
            print("PAA5100JE detected!")
        else:
            print(f" Unexpected ID: {prod_id}")

    def get_motion(self):
        """Get motion data (delta X and delta Y)."""
        dx = self.read_register(0x03)  # Motion delta X
        dy = self.read_register(0x04)  # Motion delta Y
        return dx, dy

# Initialize the sensor
sensor = PAA5100JE(spi, cs)

# Main loop: Read and print motion data
while True:
    dx, dy = sensor.get_motion()
    print(f"Delta X: {dx}, Delta Y: {dy}")
    time.sleep(0.1)
