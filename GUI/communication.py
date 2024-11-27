import serial
import time
import struct

# Open the serial port
#esp32 = serial.Serial(constants.serial_port, constants.baud_rate, timeout=1)
time.sleep(2)  # Wait for the connection to establish

#value1: is the x angle of the plate, Double
#value2: is the y angle of the plate, Double
#height: is the hight of the plate, Double
#state1: is the value of the eyes light, int
#state2: is the value of the arm light, int
#state3: is the value of the brain light, int
#homing: is a bool for starting the homing rutine.
def send_data(value1, value2, height, state1, state2, state3, homing):
    
    start_byte = b'\x02'
    # Pack the data into a binary message
    states_byte = (state1 << 2) | (state2 << 1) | state3  # Pack the three states into one byte
    homing_byte = 1 if homing else 0                      # Set homing byte (1 or 0)

    # Create the binary message
    message_body = struct.pack('>dddBB', value1, value2, height, states_byte, homing_byte)

    # Prepend the start byte to the message
    message = start_byte + message_body
    # Send the message
    #esp32.write(message)
    print(f"Sent: value1={value1}, value2={value2}, height={height}, states=({state1}, {state2}, {state3}), homing={homing}")
