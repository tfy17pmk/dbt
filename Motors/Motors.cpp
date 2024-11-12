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

void Motors::phase1() {

  std::array<bool, 3> first_time;
  first_time.fill(true);
  

  for(int i = 0; i < 3; i++) {
    // Configure the stepper motor for the initial slow homing phase
    stepper[i].setMaxSpeed(2000);   // Slow movement toward the switch
    stepper[i].setAcceleration(1000);  // Slow acceleration for initial approach
    // Homing phase 1: Move slowly toward the button (limit switch)
    stepper[i].setSpeed(1000);  // Slow speed toward the switch
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
  
  Serial.println("Limit switch hit, moving back.");
  buttonPressed.fill(false);
}

void Motors::phase2(int motor, bool first_time) {

  // Homing phase 2: Move back faster with higher acceleration
  if(first_time) {
    // Increase acceleration for faster back-off
    stepper[motor].setMaxSpeed(4000);   // Increase max speed significantly
    stepper[motor].setAcceleration(1000);
    int backOffSteps = 90;  // Approximate number of microsteps for 10 degrees (1/32 microstepping)
    stepper[motor].move(-backOffSteps);  // Move back by 10 degrees
  }else if(stepper[motor].distanceToGo() != 0) {
    stepper[motor].run();  // Run the motor while it backs off
  }
}

void Motors::phase3() {

  buttonPressed.fill(false);
  std::array<bool, 3> saved_pos;
  saved_pos.fill(false);

  for(int i = 0; i < 3; i++) {
    // Configure the stepper motor for the initial slow homing phase
    stepper[i].setMaxSpeed(200);   // Slow movement toward the switch
    stepper[i].setAcceleration(50);  // Slow acceleration for initial approach
    // Homing phase 1: Move slowly toward the button (limit switch)
    stepper[i].setSpeed(100);  // Slow speed toward the switch
  }
      
  while (!buttonPressed[0] || !buttonPressed[1] || !buttonPressed[2]) {  // Move until the button is pressed

    if(!buttonPressed[0]) {
      stepper[0].runSpeed();
    }else {
      stepper[0].setCurrentPosition(3700); // stright out 500, vertical 2100
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

void Motors::home() {

  skipPhaseOne.fill(false);
  for(int i = 0; i < 3; i++) {
    if(digitalRead(buttonPin[i]) == HIGH) {
      skipPhaseOne[i] = true;
    }
  }

  Serial.println("nu startar home!");
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

  Serial.println("Back off complete. Fine tuning...");

  phase3();
  
  Serial.println(stepper[0].currentPosition());
  Serial.println(stepper[1].currentPosition());
  Serial.println(stepper[2].currentPosition());

  initial_position();
  Serial.println("Homing complete, position set to 0.");
}

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

void Motors::set_speed(double motor_angles[3], double prev_motor_angles) {
  for (int i = 0; i < 3; i++) {
      speedPrev[i] = speed[i];                                                                                                           //sets previous speed
      speed[i] = (i == 0) * stepper[0].currentPosition() + (i == 1) * stepper[1].currentPosition() + (i == 2) * stepper[2].currentPosition();  //sets current position
      speed[i] = abs(speed[i] - motor_angles[i]) * _cs;                                                                                            //calculates the error in the current position and target position
      speed[i] = constrain(speed[i], speedPrev[i] - 200, speedPrev[i] + 200);                                                            //filters speed by preventing it from beign over 100 away from last speed
      speed[i] = constrain(speed[i], 0, _max_speed);                                                                                           //constrains sped from 0 to 1000
    }
}

void Motors::set_angle(double motor_angles[3]) {

  //float speed = 4000;
  set_speed(motor_angles, prev_motor_angles[0]);

  if (motor_angles[0] != prev_motor_angles[0]){
    _steps = floor(motor_angles[0] * _inv_degree_per_step); // convert degrees to steps
    //Serial.println(_steps);
    
    stepper[0].setMaxSpeed(speed[0]);   // Increase max speed significantly
    stepper[0].setAcceleration(speed[0]*_acc_multiplier);
    stepper[0].moveTo(_steps);
    prev_motor_angles[0] = motor_angles[0];
  }

  if (motor_angles[1] != prev_motor_angles[1]){
    _steps = floor(motor_angles[1] * _inv_degree_per_step); // convert degrees to steps
    //Serial.println(_steps);
    //float speed = set_speed(motor_angles, prev_motor_angles[1]);
    stepper[1].setMaxSpeed(speed[1]);   // Increase max speed significantly
    stepper[1].setAcceleration(speed[1]*_acc_multiplier);
    stepper[1].moveTo(_steps);
    prev_motor_angles[1] = motor_angles[1];

  }

  if (motor_angles[2] != prev_motor_angles[2]){
    _steps = floor(motor_angles[2] * _inv_degree_per_step); // convert degrees to steps
    //Serial.println(_steps);
    //float speed = set_speed(motor_angles, prev_motor_angles[2]);
    stepper[2].setMaxSpeed(speed[2]);   // Increase max speed significantly
    stepper[2].setAcceleration(speed[2]*_acc_multiplier);
    stepper[2].moveTo(_steps);
    prev_motor_angles[2] = motor_angles[2];
  }
}

void Motors::clean_up() {
    for (int i = 0; i < 3; i++) {
        ledcWrite(_STEP[i], 0); // Stop all motors
    }
}
