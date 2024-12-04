/*
 * This file is part of the ball ballancing robot.
 *
 * Developed for Curiosum during the design bulid test course, fall 2024 by 
 * project group 11.
 *
 * date: 4/12-2024
 */
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

    // set pins for calibration buttons
    std::array<int, 3> buttonPin = {25, 5, 4};
    std::array<bool, 3> buttonPressed;

    std::array<bool, 3> skipPhaseOne;

    // initialize speed and position vector
    double speed[3] = {0,0,0};
    double position[3] = {0,0,0};

private:
    // Member variables for motor control

    // Pin setup for motors First column first motor
    int _MODE[3] = {14, 32, 15};
    int _DIR[3] = {19, 27, 13};
    int _STEP[3] = {18, 33, 12};
    std::array<AccelStepper, 3> stepper;

    int _RESOLUTION[3] = {1,0,1}; // Resolution for 1/32 microstepping 
    float _inv_degree_per_step = 17.777778; // Set inverse degree per step 1/(1.8/32);

    // initialize arrays
    std::array<double, 3> _steps = {0,0,0};
    std::array<double, 3> _prev_steps = {0,0,0};
    double _speedPrev[3];
    double _diff[3] = {0,0,0};

    // initialize functions
    void set_speed(double steps[3]);
    void phase1();
    void phase2(int motor, bool first_time);
    void phase3();

    // set constants for motor characteristics
    float _max_speed = 2000;//2000
    float _cs = 50;//50
    double _acc_multiplier = 5;//5
    double _speed_diff = 100;//100

    double _prev_rec_time = 0;
};

#endif // MOTORS_H
