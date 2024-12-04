/*
 * This file is part of the ball ballancing robot.
 *
 * Developed for Curiosum during the design bulid test course, fall 2024 by 
 * project group 11.
 *
 * date: 4/12-2024
 */
#include "Arduino.h"
#include "Kinematics.h"
#include "Motors.h"
#include <AccelStepper.h>
#include <array>  // Include array library
#include <esp32-hal-cpu.h>
#include <HardwareSerial.h>

#define pi 3.1415926535

const uint8_t START_BYTE = 0x02;  

// Read the complete message (assuming 14 bytes total)
double normal_vector_x, normal_vector_y;
double height = 15;
uint8_t states_byte, homing_byte;
bool homing;
bool new_angles;

const size_t MESSAGE_LENGTH = 3 * sizeof(double) + 2 * sizeof(uint8_t);

double update_time;

Kinematics kinematics;
Motors motors;

// initialize stepper motors
std::array<AccelStepper, 3>& stepper = motors.setup_accel();
std::array<double, 3> motor_angles = {0,0,0};

// setup interupt for calibration buttons
void IRAM_ATTR handleButtonPress1() {
  motors.buttonPressed[0] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress2() {
  motors.buttonPressed[1] = true;  // Set flag when the button is pressed
}

void IRAM_ATTR handleButtonPress3() {
  motors.buttonPressed[2] = true;  // Set flag when the button is pressed
}

void setup() {
  Serial.begin(115200);
  setCpuFrequencyMhz(240);

  motors.buttonPressed.fill(false);
  motors.skipPhaseOne.fill(false);

  pinMode(motors.buttonPin[0], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[0]), handleButtonPress1, RISING);

  pinMode(motors.buttonPin[1], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[1]), handleButtonPress2, RISING);

  pinMode(motors.buttonPin[2], INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(motors.buttonPin[2]), handleButtonPress3, RISING);

  // initialize position
  motors.home(); 

  Serial.println("setup done!");
}

/*
* Description: Recieves and unpacks data send from the large computer.  
*
* Input: None
*
* Output: None
*/
void receiveData() {
  // Wait for the start byte
  if ((Serial.available() > 0) && Serial.read() == START_BYTE) {
    unsigned long startTime = millis();

    // Wait until the complete message is available or a timeout occurs
    while (Serial.available() < MESSAGE_LENGTH - 1) {
      if (millis() - startTime > 1000) { // 1-second timeout
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
    Serial.flush();

    // Process the data
    bool state1 = (states_byte & 0b100) >> 2;
    bool state2 = (states_byte & 0b010) >> 1;
    bool state3 = (states_byte & 0b001);
    homing = homing_byte == 1;
  }
  return;
}

void loop() {

  receiveData(); // receive data
  if (homing == true){
    // home and find position
    motors.home();
    homing = false;
  } else {

    // calculate motor angles
    motor_angles = kinematics.setPosition(normal_vector_x, normal_vector_y, height); 

    // set motor angles
    motors.set_angle(motor_angles.data());
    
    update_time = millis();
    // Run latets set position in 2ms
    while (millis() - update_time < 2){
      stepper[0].run();
      stepper[1].run();
      stepper[2].run();
    }
  }
}

