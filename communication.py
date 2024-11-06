import serial
import time
import struct

class Commmunication:
    def __init__(self):
        
        # Replace with the port your ESP32 is connected to
        self.serial_ports = [f"/dev/ttyUSB{i}" for i in range(5)]  # Use 'ls /dev/tty.*' to find the correct port
        self.baud_rate = 115200  # Make sure this matches the Arduino's baud rate

        # Open the serial port
        self.esp32 = None
        self.connect()#serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        time.sleep(1)  # Wait for the connection to establish

    def connect(self):
        for port in self.serial_ports:
            try:
                self.esp32 = serial.Serial(port, self.baud_rate, timeout=1)
                print(f"Connected to USB{port}.")
            except serial.SerialException:
                pass
        time.sleep(1)
    
        if self.esp32 is None:
            print("Could not connect to ESP.")
            exit(1)
        


    def send_data(self, value1, value2, height, state1, state2, state3, homing):
        start_byte = b'\x02'
        
        # Pack the state and homing information
        states_byte = (state1 << 2) | (state2 << 1) | state3  # Pack the three states into one byte
        homing_byte = 1 if homing else 0                      # Set homing byte (1 or 0)
        
        # Pack the data into a binary message
        message_body = struct.pack('<dddBB', value1, value2, height, states_byte, homing_byte)
        
        # Prepend the start byte to the message
        message = start_byte + message_body
        
        # Send the message
        self.esp32.write(message)
        #esp32.flush()
        print(f"Sent: value1={value1}, value2={value2}, height={height}, states=({state1}, {state2}, {state3}), homing={homing}")
        

    def receive_response(self):
        try:
            # Wait to receive the start byte
            while True:
                if self.esp32.read() == b'\x02':  # Start byte
                    # Read the rest of the message
                    response = self.esp32.read(struct.calcsize('<dddBB'))
                    if len(response) == struct.calcsize('<dddBB'):
                        # Unpack the response data
                        theta, phi, height, states_byte, homing_byte = struct.unpack('<dddBB', response)
                        
                        # Extract states and homing values
                        state1 = (states_byte & 0b100) >> 2
                        state2 = (states_byte & 0b010) >> 1
                        state3 = (states_byte & 0b001)
                        homing = bool(homing_byte)
                        
                        # Print the received values
                        print("Received:")
                        print(f"theta={theta}, phi={phi}, height={height}")
                        print(f"states=({state1}, {state2}, {state3}), homing={homing}")
                        break
        except struct.error as e:
            print(f"Unpacking error: {e}")

if __name__ == "__main__":
    com = Commmunication()
    try:
        # Example usage
        com.send_data(0, 0, 15, 1, 0, 1, False)
        # Read and unpack the response
        com.receive_response()
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        com.esp32.close()