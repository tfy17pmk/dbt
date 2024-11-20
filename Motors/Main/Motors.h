#ifndef MOTORS_H
#define MOTORS_H

#include "Arduino.h"
#include <AccelStepper.h>
#include <array>

class Motors {
public:
    // Constructor to initialize motors with mode, direction, and step pins
    Motors();
    void initial_position();
    std::array<AccelStepper, 3>& setup_accel();
    void set_angle(double motor_angles[3]);
    void home();
    void IRAM_ATTR handleButtonPress1();
    void IRAM_ATTR handleButtonPress2();
    void IRAM_ATTR handleButtonPress3();

    //const int _buttonPin1 = 25;    // Button pin (limit switch or homing switch)

    //const int _buttonPin2 = 5;    // Button pin (limit switch or homing switch)

    //const int _buttonPin3 = 4;    // Button pin (limit switch or homing switch)
    std::array<int, 3> buttonPin = {25, 5, 4};
    std::array<bool, 3> buttonPressed;
    std::array<bool, 3> skipPhaseOne;
    double speed1[3] = {0,0,0};
    double speed2[3] = {0,0,0};
    double speed3[3] = {0,0,0};
    double speed[3] = {0,0,0};

    double position[3] = {0,0,0};
    double _diff[3] = {0,0,0};




private:
    // Member variables for motor control

    // Pin setup for motors First column first motor
    int _MODE[3] = {14, 32, 15};
    int _DIR[3] = {19, 27, 13};
    int _STEP[3] = {18, 33, 12};
    std::array<AccelStepper, 3> stepper;

    int _RESOLUTION[3] = {1,0,1}; // Resolution for 1/32 microstepping 
    float _inv_degree_per_step = 17.777778; // Set inverse degree per step 1/(1.8/32);
    std::array<double, 3> _steps = {0,0,0};
    std::array<double, 3> prev_steps = {0,0,0};
    void set_speed(double steps[3]);
    float _max_speed = 2000;//2000
    float _cs = 70;//50
    double _acc_multiplier = 5;//5
    double _speed_diff = 100;//100
    double speedPrev[3];
    double prev_rec_time = 0;

    void phase1();
    void phase2(int motor, bool first_time);
    void phase3();

};

#endif // MOTORS_H
