#include "Arduino.h"
#include "Kinematics.h"
#include "Motors.h"
#include <AccelStepper.h>
#include <array>  // Include array library
#include <esp32-hal-cpu.h>

#define pi 3.1415926535

Kinematics kinematics;
Motors motors;
//AccelStepper stepper1 = motors.setup_homing();

void IRAM_ATTR handleButtonPress1() {
  motors.buttonPressed[0] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress2() {
  motors.buttonPressed[1] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress3() {
  motors.buttonPressed[2] = true;  // Set flag when the button is pressed
}

  HardwareSerial SerialPort(1);   // Use UART1 on ESP32
// Interrupt Service Routine (ISR) for the button

void setup() {
  Serial.begin(115200);
  setCpuFrequencyMhz(160);
  motors.setup_homing();

  motors.buttonPressed.fill(false);

  // Initialize UART1 for communication with Raspberry Pi
  SerialPort.begin(115200, SERIAL_8N1, 16, 17);  // UART1: TX=GPIO17, RX=GPIO16
  pinMode(motors._buttonPin1, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors._buttonPin1), handleButtonPress1, RISING);

  pinMode(motors._buttonPin2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors._buttonPin2), handleButtonPress2, RISING);

  pinMode(motors._buttonPin3, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors._buttonPin3), handleButtonPress3, RISING);

  // Configure the stepper motor for the initial slow homing phase
  //stepper1.setMaxSpeed(500);   // Slow movement toward the switch
  //stepper1.setAcceleration(100);  // Slow acceleration for initial approach

  //if(digitalRead(motors._buttonPin1) == HIGH) {
    //motors._skipPhaseOne1 = true;
  //}

  // initialize position
  motors.initial_position(); // Set initial position of the motors

  /*
  const int pin_direction_motor1 = 19;
  const int pin_direction_motor2 = 27;
  const int pin_direction_motor3 = 13;

  const int pin_step_motor1 = 18;
  const int pin_step_motor2 = 33;
  const int pin_step_motor3 = 12;

  const int Mode1 = 14;
  const int Mode2 = 32;
  const int Mode3 = 15;
  */
  

  std::array<double, 3> motor_angles = kinematics.setPosition(20*pi/180, 20*pi/180);

  // Print the motor angles
  for (size_t i = 0; i < motor_angles.size(); ++i) {
      Serial.print("Motor angle ");
      Serial.print(i);
      Serial.print(": ");
      Serial.println(motor_angles[i]);
  }

  /*
  Serial.println(motor_angle[0]);
  Serial.println(motor_angle[1]);
  Serial.println(motor_angle[2]);
  */

  Serial.println("setup done!");

}

void loop() {

  if (SerialPort.available()) {
    char receivedChar = SerialPort.read();  // Read data from Raspberry Pi
    Serial.print("Received: ");             // Print debug message
    Serial.println(receivedChar);           // Show the received character
    
    Serial.println(receivedChar);

    if(receivedChar == '0'){
      motors.home();
      Serial.println("fick en 0a");
    }
    
  }

  //float goal_angles[3] = {1, 1, 1};
  //motors.set_angle(goal_angles);
  }

