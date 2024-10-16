#include "Arduino.h"
#include "Motors.h"

// Constructor to initialize motors with mode, direction, and step pins
Motors::Motors(int modePins[], int dirPins[], int stepPins[]) {
    for (int i = 0; i < 3; i++) {
      
        MODE[i] = modePins[i];
        DIR[i] = dirPins[i];
        STEP[i] = stepPins[i];

        pinMode(MODE[i], OUTPUT);
        pinMode(DIR[i], OUTPUT);
        //pinMode(_STEP[i], OUTPUT);
        digitalWrite(STEP[i], LOW); // Initialize step pins to low
        digitalWrite(MODE[i], RESOLUTION[i]);

        // Set the PWM frequency
        ledcSetup(i, PWM_frequency, 8); // 8-bit resolution
        ledcAttachPin(STEP[i], i); // Attach the step pin to the channel
    }
}


void Motors::initial_position() {
    for (int i = 0; i < 3; i++) {
        current_angles[i] = 20.0; // Initialize current angles to 20 degrees
    }
}

void Motors::set_angle(float goal_angles[3]) {
    for (int i = 0; i < 3; i++) {
        relative_angles[i] = goal_angles[i] - current_angles[i];
        current_angles[i] = goal_angles[i];
        required_steps[i] = abs(relative_angles[i]) / degree_per_step; // Convert angle to steps
        rotation_times[i] = required_steps[i] * 1000000 / PWM_frequency; // Calculate rotation times
        step_direction[i] = (relative_angles[i] > 0) ? 0 : 1; // Determine step direction
    }

    for (int i = 0; i < 3; i++) {
        if (relative_angles[i] != 0) {
            digitalWrite(DIR[i], step_direction[i]); // Set direction
            delay(1); // Short delay for motor stabilization
            ledcWrite(STEP[i], PWM_duty); // Start stepping
        }
    }

    unsigned long start_tick = millis();
    unsigned long max_rotation_time = 0;
    for (int i = 0; i < 3; i++) {
        if (rotation_times[i] > max_rotation_time) {
            max_rotation_time = rotation_times[i];
        }
    }

    while (millis() - start_tick < max_rotation_time) {
        for (int i = 0; i < 3; i++) {
            if (millis() - start_tick >= rotation_times[i]) {
                ledcWrite(STEP[i], 0); // Stop stepping for this motor
            }
        }
    }

    // Stop all motors after completing the rotation
    for (int i = 0; i < 3; i++) {
        ledcWrite(STEP[i], 0); // Set PWM to 0
    }
}

void Motors::clean_up() {
    for (int i = 0; i < 3; i++) {
        ledcWrite(STEP[i], 0); // Stop all motors
    }
}
