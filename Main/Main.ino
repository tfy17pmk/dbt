#include "Arduino.h"
#include "Kinematics.h"
#include "InverseKinematics.h" // not ours
#include "Motors.h"
#include <AccelStepper.h>
#include <array>  // Include array library
#include <esp32-hal-cpu.h>
#include <HardwareSerial.h>


#define pi 3.1415926535

#define LED 2

const uint8_t START_BYTE = 0x02;  

// Read the complete message (assuming 14 bytes total)
double normal_vector_x, normal_vector_y, height;
uint8_t states_byte, homing_byte;
bool homing;
bool new_angles;

const size_t MESSAGE_LENGTH = 3 * sizeof(double) + 2 * sizeof(uint8_t);




Kinematics kinematics;
Motors motors;
std::array<AccelStepper, 3>& stepper = motors.setup_accel();
std::array<double, 3> motor_angles = {0,0,0};
std::array<double, 3> prev_motor_angles = {0,0,0};


void IRAM_ATTR handleButtonPress1() {
  motors.buttonPressed[0] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress2() {
  motors.buttonPressed[1] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress3() {
  motors.buttonPressed[2] = true;  // Set flag when the button is pressed
}

//  HardwareSerial SerialPort(1);   // Use UART1 on ESP32
// Interrupt Service Routine (ISR) for the button

void setup() {
  Serial.begin(115200);
  //SerialPort.begin(115200, SERIAL_8N1, 16, 17);
  setCpuFrequencyMhz(160);
  // Set pin mode
  pinMode(LED_BUILTIN,OUTPUT);

  motors.buttonPressed.fill(false);
  motors.skipPhaseOne.fill(false);

  // Initialize UART1 for communication with Raspberry Pi
  //SerialPort.begin(115200, SERIAL_8N1, 16, 17);  // UART1: TX=GPIO17, RX=GPIO16
  pinMode(motors.buttonPin[0], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[0]), handleButtonPress1, RISING);

  pinMode(motors.buttonPin[1], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[1]), handleButtonPress2, RISING);

  pinMode(motors.buttonPin[2], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[2]), handleButtonPress3, RISING);

  // initialize position
  motors.home(); 

  // Print the motor angles
  for (size_t i = 0; i < motor_angles.size(); ++i) {
      Serial.print("Motor angle ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(motor_angles[i]);
  }

  Serial.println("setup done!");

}

void receiveData() {
  // Wait for the start byte
  if ((Serial.available() > 0) && Serial.read() == START_BYTE) {
    unsigned long startTime = millis();

    // Wait until the complete message is available or a timeout occurs
    while (Serial.available() < MESSAGE_LENGTH - 1) {
      if (millis() - startTime > 1000) { // 1-second timeout
        Serial.println("Timeout! Discarding incomplete message.");
        Serial.flush();
        return;
      }
    }

    // Read and unpack the data
    Serial.readBytes((char*)&normal_vector_x, sizeof(double));
    Serial.readBytes((char*)&normal_vector_y, sizeof(double));
    Serial.readBytes((char*)&height, sizeof(double));
    Serial.readBytes((char*)&states_byte, 1);
    Serial.readBytes((char*)&homing_byte, 1);

    // Process the data
    bool state1 = (states_byte & 0b100) >> 2;
    bool state2 = (states_byte & 0b010) >> 1;
    bool state3 = (states_byte & 0b001);
    homing = homing_byte == 1;

    // Print received values for debugging
    Serial.print("Received: normal_vector_x=");
    Serial.print(normal_vector_x);
    Serial.print(", normal_vector_y=");
    Serial.print(normal_vector_y);
    Serial.print(", height=");
    Serial.print(height);
    Serial.print(", states=(");
    Serial.print(state1);
    Serial.print(", ");
    Serial.print(state2);
    Serial.print(", ");
    Serial.print(state3);
    Serial.print("), homing=");
    Serial.println(homing);

    // Trigger action based on received data
    /*
    if (theta == 10) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(2000);
      digitalWrite(LED_BUILTIN, LOW);
    }
    */

    // Send back the received data
    Serial.write(START_BYTE);  // Start byte for the response
    Serial.write((const char*)&normal_vector_x, sizeof(double));
    Serial.write((const char*)&normal_vector_y, sizeof(double));
    Serial.write((const char*)&height, sizeof(double));
    Serial.write(states_byte);  // Send back the states byte
    Serial.write(homing_byte);  // Send back the homing byte

    Serial.println("Data echoed back to sender.");
  }
  return;
}

void loop() {

  receiveData();
  if (homing == true){
    motors.home();
    homing = false;
  } else {
    
    motor_angles = kinematics.setPosition(normal_vector_x, normal_vector_y); // input rad; return degree

    // check for only setting speed acceleration once for each motor angles set
    if ((motor_angles[0] != prev_motor_angles[0]) && (motor_angles[1] != prev_motor_angles[1]) && (motor_angles[2] != prev_motor_angles[2])){
      // Print the motor angles
      for (size_t i = 0; i < motor_angles.size(); ++i) {
        Serial.print("Motor angle ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(motor_angles[i]);
        prev_motor_angles[i] = motor_angles[i];
      }      
      motors.set_angle(motor_angles.data());
    }

    stepper[0].run();
    stepper[1].run();
    stepper[2].run();

  }
}

