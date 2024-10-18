#include "Arduino.h"
#include "Motors.h"

// Constructor to initialize motors with mode, direction, and step pins
Motors::Motors() {
    for (int i = 0; i < 3; i++) {

        pinMode(_MODE[i], OUTPUT);
        pinMode(_DIR[i], OUTPUT);
        //pinMode(_STEP[i], OUTPUT);
        digitalWrite(_STEP[i], LOW); // Initialize step pins to low
        digitalWrite(_MODE[i], _RESOLUTION[i]);

        // Set the PWM frequency
        //ledcSetup(i, PWM_frequency, 8); // 8-bit resolution
        //ledcAttachPin(STEP[i], i); // Attach the step pin to the channel
    }
}


void Motors::setup_homing() {
  AccelStepper tmp_stepper1(AccelStepper::DRIVER, _STEP[0], _DIR[0]);  // Set up the AccelStepper for DRV8825
  AccelStepper tmp_stepper2(AccelStepper::DRIVER, _STEP[1], _DIR[1]);  // Set up the AccelStepper for DRV8825
  AccelStepper tmp_stepper3(AccelStepper::DRIVER, _STEP[2], _DIR[2]);  // Set up the AccelStepper for DRV8825
  
  stepper[0] = tmp_stepper1;
  stepper[1] = tmp_stepper2;
  stepper[2] = tmp_stepper3;
  //return tmp_stepper1;
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

    if(!buttonPressed[0]) {
      stepper[0].runSpeed();
    }else if(buttonPressed[0]) {
      phase2(0, first_time[0]);
      first_time[0] = false;
    }

    if(!buttonPressed[1]) {
      stepper[1].runSpeed();
    }else {
      phase2(1, first_time[1]);
      first_time[1] = false;
    }

    if(!buttonPressed[2]) {
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
      stepper[0].setCurrentPosition(0);
      saved_pos[0] = true;
    }

    if(!buttonPressed[1]) {
      stepper[1].runSpeed();
    }else {
      stepper[1].setCurrentPosition(0);
      saved_pos[1] = true;
    }

    if(!buttonPressed[2]) {
      stepper[2].runSpeed();
    }else {
      stepper[2].setCurrentPosition(0);
      saved_pos[2] = true;
    }

  }

  for(int i = 0; i < 3; i++) {
    if(!saved_pos[i]) {
      stepper[i].setCurrentPosition(0);
    }
  }

}

void Motors::home() {
  static bool homingComplete = false;
  buttonPressed[0] = false;
  buttonPressed[1] = false;
  buttonPressed[2] = false;

  if (!homingComplete) {
    if(!_skipPhaseOne1) {
      phase1();
    }

    while(stepper[0].distanceToGo() != 0 || stepper[1].distanceToGo() != 0 || stepper[2].distanceToGo() != 0) {
      for(int i = 0; i < 3; i++) {

        if(stepper[i].distanceToGo() != 0) {
          phase2(i, false);
        }
      }
    }

    Serial.println("Back off complete. Fine tuning...");

    phase3();

    // Homing phase 3: Use interrupt-based fine-tuning but with slower movement
    // Homing complete: Save the current position
    // Set this as the home position
    Serial.println("Homing complete, position set to 0.");
    homingComplete = true;  // Mark homing as complete
  }

}


void Motors::initial_position() {
    for (int i = 0; i < 3; i++) {
        _current_angles[i] = 20.0; // Initialize current angles to 20 degrees
    }
}

void Motors::set_angle(float goal_angles[3]) {
    for (int i = 0; i < 3; i++) {
        _relative_angles[i] = goal_angles[i] - _current_angles[i];
        _current_angles[i] = goal_angles[i];
        _required_steps[i] = abs(_relative_angles[i]) / _degree_per_step; // Convert angle to steps
        _rotation_times[i] = _required_steps[i] * 1000000 / _PWM_frequency; // Calculate rotation times
        _step_direction[i] = (_relative_angles[i] > 0) ? 0 : 1; // Determine step direction
    }

    for (int i = 0; i < 3; i++) {
        if (_relative_angles[i] != 0) {
            digitalWrite(_DIR[i], _step_direction[i]); // Set direction
            delay(1); // Short delay for motor stabilization
            ledcWrite(_STEP[i], _PWM_duty); // Start stepping
        }
    }

    unsigned long start_tick = millis();
    unsigned long max_rotation_time = 0;
    for (int i = 0; i < 3; i++) {
        if (_rotation_times[i] > max_rotation_time) {
            max_rotation_time = _rotation_times[i];
        }
    }

    while (millis() - start_tick < max_rotation_time) {
        for (int i = 0; i < 3; i++) {
            if (millis() - start_tick >= _rotation_times[i]) {
                ledcWrite(_STEP[i], 0); // Stop stepping for this motor
            }
        }
    }

    // Stop all motors after completing the rotation
    for (int i = 0; i < 3; i++) {
        ledcWrite(_STEP[i], 0); // Set PWM to 0
    }
}

void Motors::clean_up() {
    for (int i = 0; i < 3; i++) {
        ledcWrite(_STEP[i], 0); // Stop all motors
    }
}
