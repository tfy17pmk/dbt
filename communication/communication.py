import serial
import time
import struct

class Commmunication:
    """Class for communication with the ESP32 microcontroller."""

    def __init__(self):
        """Initialize the communication class."""
        self.serial_ports = [f"/dev/ttyUSB{i}" for i in range(5)]  # Use 'ls /dev/tty*' to find the correct port
        self.baud_rate = 115200

        # Open the serial port and wait for the connection to establish
        self.esp32 = None
        self.connect()
        time.sleep(1)

    def connect(self):
        """Find the correct serial port and connect to the ESP32."""
        for port in self.serial_ports:
            try:
                self.esp32 = serial.Serial(port, self.baud_rate, timeout=1)
                print(f"Connected to USB{port}.")
            except serial.SerialException:
                pass
    
        if self.esp32 is None:
            print("Could not connect to ESP.")
            exit(1)
        
    def send_data(self, value1, value2, height, state1, state2, state3, homing):
        """Send data to the ESP32 microcontroller."""
        start_byte = b'\x02'
        
        # Pack the state and homing information
        states_byte = (state1 << 2) | (state2 << 1) | state3  # Pack the three states into one byte
        homing_byte = 1 if homing else 0
        
        # Pack the data into a binary message
        message_body = struct.pack('<dddBB', value1, value2, height, states_byte, homing_byte)
        
        # Prepend the start byte to the message
        message = start_byte + message_body
        
        # Send the message
        self.esp32.write(message)