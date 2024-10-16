#include "Arduino.h"
#include "Motors.h"

// Constructor to initialize motors with mode, direction, and step pins
Motors::Motors(int modePins[3], int dirPins[3], int stepPins[3]) {
    for (int i = 0; i < 3; i++) {
        _MODE[i] = modePins[i];
        _DIR[i] = dirPins[i];
        _STEP[i] = stepPins[i];

        pinMode(_MODE[i], OUTPUT);
        pinMode(_DIR[i], OUTPUT);
        pinMode(_STEP[i], OUTPUT);
        digitalWrite(_STEP[i], LOW); // Initialize step pins to low
        digitalWrite(_MODE[i], _RESOLUTION[i])
        // Set the PWM frequency
        ledcAttach(_STEP[i], _PWM_frequency, 8); // Set PWM frequency
        ledcWrite(_STEP[i], 0); // Set initial PWM duty cycle to 0
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
        _step_direction[i] = (relative_angles[i] > 0) ? 0 : 1; // Determine step direction
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
