/*
 * This file is part of the ball ballancing robot.
 *
 * Developed for Curiosum during the design bulid test course, fall 2024 by 
 * project group 11.
 *
 * date: 4/12-2024
 */
#include "AccelStepper.h"
#include "Arduino.h"
#include "Motors.h"

// Constructor to initialize motors with mode, direction, and step pins
Motors::Motors() {
    for (int i = 0; i < 3; i++) {

      pinMode(_MODE[i], OUTPUT);
      pinMode(_DIR[i], OUTPUT);
      digitalWrite(_STEP[i], LOW); // Initialize step pins to low
      digitalWrite(_MODE[i], _RESOLUTION[i]);
    }
}


std::array<AccelStepper, 3>& Motors::setup_accel() {
  AccelStepper tmp_stepper1(AccelStepper::DRIVER, _STEP[0], _DIR[0]);  // Set up the AccelStepper for DRV8825
  AccelStepper tmp_stepper2(AccelStepper::DRIVER, _STEP[1], _DIR[1]);  // Set up the AccelStepper for DRV8825
  AccelStepper tmp_stepper3(AccelStepper::DRIVER, _STEP[2], _DIR[2]);  // Set up the AccelStepper for DRV8825
  
  stepper[0] = tmp_stepper1;
  stepper[1] = tmp_stepper2;
  stepper[2] = tmp_stepper3;
  return stepper;
}

/*
* Description: Performs first phase of the homing routine, moves arms down until buttons are pressed. 
*
* Input: None
*
* Output: None
*/
void Motors::phase1() {

  std::array<bool, 3> first_time;
  first_time.fill(true);
  

  for(int i = 0; i < 3; i++) {
    // Configure the stepper motor for the initial slow homing phase
    stepper[i].setMaxSpeed(2000);       // Slow movement toward the switch
    stepper[i].setAcceleration(1000);   // Slow acceleration for initial approach
    // Homing phase 1: Move slowly toward the button (limit switch)
    stepper[i].setSpeed(1000);          // Slow speed toward the switch
  }
      
  while (!buttonPressed[0] || !buttonPressed[1] || !buttonPressed[2]) {  // Move until the button is pressed

    if(!buttonPressed[0] && !skipPhaseOne[0]) {
      stepper[0].runSpeed();
    }else {
      phase2(0, first_time[0]);
      first_time[0] = false;
    }

    if(!buttonPressed[1] && !skipPhaseOne[1]) {
      stepper[1].runSpeed();
    }else {
      phase2(1, first_time[1]);
      first_time[1] = false;
    }

    if(!buttonPressed[2] && !skipPhaseOne[2]) {
      stepper[2].runSpeed();
    }else {
      phase2(2, first_time[2]);
      first_time[2] = false;
    }

  }

  for(int i = 0; i < 3; i++) {
    if(first_time[i]) {
      phase2(i, first_time[i]);
    }
  }
  buttonPressed.fill(false);
}

/*
* Description: Performs second phase of the homing routine, moves arms up a small amount. 
*
* Input: a motor and if it is the first time, which implies that maxspeed and acceleration has to be set.
*
* Output: None
*/
void Motors::phase2(int motor, bool first_time) {

  // Homing phase 2: Move back faster with higher acceleration
  if(first_time) {
    // Increase acceleration for faster back-off
    stepper[motor].setMaxSpeed(4000);           // Increase max speed significantly
    stepper[motor].setAcceleration(1000);
    int backOffSteps = 90;                      // Approximate number of microsteps for 10 degrees (1/32 microstepping)
    stepper[motor].move(-backOffSteps);         // Move back by 10 degrees
  }else if(stepper[motor].distanceToGo() != 0) {
    stepper[motor].run();                       // Run the motor while it backs off
  }
}

/*
* Description: Performs third phase of the homing routine, moves arms down again slowly and then go to initial position 
*
* Input: None
*
* Output: None
*/
void Motors::phase3() {

  buttonPressed.fill(false);
  std::array<bool, 3> saved_pos;
  saved_pos.fill(false);

  for(int i = 0; i < 3; i++) {
    // Configure the stepper motor for the initial slow homing phase
    stepper[i].setMaxSpeed(200);      // Slow movement toward the switch
    stepper[i].setAcceleration(50);   // Slow acceleration for initial approach
    stepper[i].setSpeed(100);         // Slow speed toward the switch
  }
      
  while (!buttonPressed[0] || !buttonPressed[1] || !buttonPressed[2]) {  // Move until the button is pressed

    if(!buttonPressed[0]) {
      stepper[0].runSpeed();
    }else {
      stepper[0].setCurrentPosition(3700); 
      saved_pos[0] = true;
    }

    if(!buttonPressed[1]) {
      stepper[1].runSpeed();
    }else {
      stepper[1].setCurrentPosition(3700);
      saved_pos[1] = true;
    }

    if(!buttonPressed[2]) {
      stepper[2].runSpeed();
    }else {
      stepper[2].setCurrentPosition(3700);
      saved_pos[2] = true;
    }

  }

  for(int i = 0; i < 3; i++) {
    if(!saved_pos[i]) {
      stepper[i].setCurrentPosition(3700);
    }
  }

}

/*
* Description: Performs a homing routine, where endpoint of motion boundary are found, adn thereby performs a calibration
*
* Input: None
*
* Output: None
*/
void Motors::home() {

  skipPhaseOne.fill(false);
  for(int i = 0; i < 3; i++) {
    if(digitalRead(buttonPin[i]) == HIGH) {
      skipPhaseOne[i] = true;
    }
  }
  
  bool homingComplete = false;
  buttonPressed.fill(false);

  phase1();

  //finish/run phase 2 depending on if the button is pressed from the beginning.
  while(stepper[0].distanceToGo() != 0 || stepper[1].distanceToGo() != 0 || stepper[2].distanceToGo() != 0) {
    for(int i = 0; i < 3; i++) {

      if(stepper[i].distanceToGo() != 0) {
        phase2(i, false);
      }
    }
  }

  phase3();

  initial_position();
}

/*
* Description: Sets initial position of table
*
* Requirement: A succesfull homing routine has to be performed to find initial position succesfully
*
* Input: None
*
* Output: None
*/
void Motors::initial_position() {

  for(int i = 0; i < 3; i++) {
    stepper[i].setMaxSpeed(4000);   // Increase max speed significantly
    stepper[i].setAcceleration(3000);
    stepper[i].moveTo(3200);   
  }
  while((stepper[0].currentPosition() != 3200) || (stepper[1].currentPosition() != 3200) || (stepper[2].currentPosition() != 3200)){
    stepper[0].run();
    stepper[1].run();
    stepper[2].run();
  }
}

/*
* Description: Calculates max speed of each motor and constrains it to be within boundaries
*
* Input: Wanted motor position in steps
*
* Output: None
*/
void Motors::set_speed(double steps[3]) {
  for (int i = 0; i < 3; i++) {
    _speedPrev[i] = speed[i];                                                                 //sets previous speed
    position[i] = stepper[i].currentPosition();                                               //sets current position
    _diff[i] =  abs(position[i] - steps[i]);                                                  //claculate the difference between current and target position of motor
    speed[i] = _diff[i] * _diff[i] * _cs;                                                    
    speed[i] = constrain(speed[i], _speedPrev[i] - _speed_diff, _speedPrev[i] + _speed_diff); //filters speed by constraining the speed to have a maximum differeence to previous 
    speed[i] = constrain(speed[i], 0, _max_speed);                                            // constrain maxspeed to be within boundaries
    }
}

/*
* Description: Calculates how many steps each motor has to take to reach the wanted 
* motor angles and sets the speed and acceleration of each motor. 
*
* Input: Wanted motor angles
*
* Output: None
*/
void Motors::set_angle(double motor_angles[3]) {

  for(int i = 0; i < 3; i++) {
    _steps[i] = floor(motor_angles[i] * _inv_degree_per_step);
  }
  set_speed(_steps.data());

  // reset maxspeed and acceleration if no new angle has been recieved in 3 seconds
  if ((millis() - _prev_rec_time) > 3000){
    for(int i = 0; i < 3; i++) {
      stepper[i].setMaxSpeed(4000);   // Increase max speed significantly
      stepper[i].setAcceleration(3000);
    }
    _prev_steps = {0,0,0};
  }

  // Set maxspeed, acceleration and wanted motor position for each motor
  if (_steps[0] != _prev_steps[0]){
    stepper[0].setMaxSpeed(speed[0]);   
    stepper[0].setAcceleration(speed[0]*_acc_multiplier);
    stepper[0].moveTo(_steps[0]);
    _prev_steps[0] = _steps[0];

    // if calculated speed is nan, use previous speed
    if (isnan(stepper[0].speed())) {
      stepper[0].setSpeed(_speedPrev[0]);
      initial_position();
    }  
  }

  if (_steps[1] != _prev_steps[1]){
    stepper[1].setMaxSpeed(speed[1]);   
    stepper[1].setAcceleration(speed[1]*_acc_multiplier);
    stepper[1].moveTo(_steps[1]);
    _prev_steps[1] = _steps[1];

    // if calculated speed is nan, use previous speed
    if (isnan(stepper[1].speed())) {
      stepper[1].setSpeed(_speedPrev[1]);
      initial_position();
    }  
  }

  if (_steps[2] != _prev_steps[2]){
    stepper[2].setMaxSpeed(speed[2]);  
    stepper[2].setAcceleration(speed[2]*_acc_multiplier);
    stepper[2].moveTo(_steps[2]);
    _prev_steps[2] = _steps[2];

    // if calculated speed is nan, use previous speed
    if (isnan(stepper[2].speed())) {
      stepper[2].setSpeed(_speedPrev[2]);
      initial_position();
    }  
  }
  _prev_rec_time = millis();
}

