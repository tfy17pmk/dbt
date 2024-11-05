import serial
import time
import struct

# Replace with the port your ESP32 is connected to
serial_port = "/dev/tty.usbserial-0199B457"  # Use 'ls /dev/tty.*' to find the correct port
baud_rate = 115200  # Make sure this matches the Arduino's baud rate

# Open the serial port
esp32 = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the connection to establish

def send_data(value1, value2, height, state1, state2, state3, homing):
    start_byte = b'\x02'
    
    # Pack the state and homing information
    states_byte = (state1 << 2) | (state2 << 1) | state3  # Pack the three states into one byte
    homing_byte = 1 if homing else 0                      # Set homing byte (1 or 0)
    
    # Pack the data into a binary message
    message_body = struct.pack('>dddBB', value1, value2, height, states_byte, homing_byte)
    
    # Prepend the start byte to the message
    message = start_byte + message_body
    
    # Send the message
    esp32.write(message)
    print(f"Sent: value1={value1}, value2={value2}, height={height}, states=({state1}, {state2}, {state3}), homing={homing}")
    
    # Read and unpack the response
    receive_response()

def receive_response():
    try:
        # Wait to receive the start byte
        while True:
            if esp32.read() == b'\x02':  # Start byte
                # Read the rest of the message
                response = esp32.read(struct.calcsize('>dddBB'))
                if len(response) == struct.calcsize('>dddBB'):
                    # Unpack the response data
                    theta, phi, height, states_byte, homing_byte = struct.unpack('>dddBB', response)
                    
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

try:
    # Example usage
    send_data(12.34, 56.78, 100.0, 1, 0, 1, True)
except serial.SerialException as e:
    print(f"Serial error: {e}")
finally:
    esp32.close()