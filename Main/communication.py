import serial
import time

# Replace with the port your ESP32 is connected to
serial_port = "/dev/tty.usbserial-0199B457"  # Use 'ls /dev/tty.*' to find the correct port AND you cant have serial monitor on in Arduino IDE!
baud_rate = 115200  # Same baud rate as in Arduino IDE

try:
    # Open the serial port
    esp32 = serial.Serial(serial_port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for the connection to establish

    print("Connected to ESP32. Type 'exit' to quit.")

    # Continuous loop to get user input
    while True:
        # Get user input
        user_input = input("Enter message to send to ESP32: ")

        # Exit the loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        # Send data to ESP32
        esp32.write(user_input.encode('utf-8'))  # Convert the message to bytes and send
        print(f"Sent: {user_input}")

        # Optionally, wait for a response from ESP32 and print it
        if esp32.in_waiting > 0:
            response = esp32.readline().decode('utf-8').strip()  # Read and decode the response
            print(f"Received from ESP32: {response}")

except serial.SerialException as e:
    print(f"Error connecting to {serial_port}: {e}")
finally:
    if 'esp32' in locals() and esp32.is_open:
        esp32.close()  # Close the serial connection
        print("Connection closed.")
