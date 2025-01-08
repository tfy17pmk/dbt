# DBT project, Ball Balancing Robot (Curiosum)

We are using Python virtual environment for development throughout the project. All the dependencies are defined in requirements.txt file, which ensures that everybody works with the same versions of dependencies. 

As for now, we have a single global virtual environment for the entire repo.

## Prerequisites

### Python version
Ensure that you use python3. Preferable version Python 3.11.2, but later versions should also be okay.

### Pip
Pip3 should be installed, if not, install with:
```
sudo apt update
sudo apt install python3-pip
pip3 --version (verify version)
```

## First setup:

### Creating environment
```
python3 -m venv dbt-venv (Linux)
python -m venv dbt-venv (Windows)
```

### Activating environment
```
source dbt-venv/bin/activate (Linux)
.\venv\Scripts\activate (Windows)
```

### Installing dependencies
```
pip install -r requirements.txt
```

## Everyday usage
Once virtual environment is created and dependencies are installed, you can follow the steps:

### Activate environment
```
source dbt-venv/bin/activate (Linux)
.\dbt-venv\Scripts\activate (Windows)
```

If you are using Windows, and get a problem with permission to run the Virtual Environment, use command:
```
Set-ExecutionPolicy Unrestricted -Scope Process
```
It can happen that you need to use it every time you open/reopen a new terminal session.

### Run applications within the environmet
```
python3 my_app.py (Linux)
python my_app.py (Windows)
```

### Deactivate environment
```
deactivate
```

## Updating dependencies
If there is a need to update the dependencies, add the new dependency to requirement.txt file.

### Update dependencies manually (Preferrable)
Add dependency on the new line in requirements.txt

### Update dependencies automatically
Otherwise, if you install the new dependency with
```
pip install new-dependency
```
add the new dependency to requirements.txt with
```
pip freeze > requirements.txt
```

OBS! Make sure to not add the dependencies that are not used/needed, if you intalled some now unused dependency before!

Don't forget to commit and push in the end of the day.

## Start program from new terminal
To start the program from a new terminal run the command:
```/home/curiadm/start_gui.sh```
It will start the program with the correct environment. 

## Maintenance of program
Password is the standard password. 
### Change text
To change the text of the pages go to ```GUI/constants.py``` here all text of the program is defined. If the text is changed be careful to check that the layout of the pages are still correct, or if the text has been changed to something that do not fit in the current canvas size. 


## Program structure
The program uses two seperate processing devices and two different programming languages python and C++

* One Standard computer (python)
* One ESP 32 feather (C++)

The two processing devices communicate between each other using serial communication. The standard computer is responsible for running the GUI, performing image processing and performing most of the computations. The script is based around three processes and queues for robust communication between the processes. 

1. One process for navigation between the different pages in the GUI and performing the different functions in the backend of the buttons. For the backend functions in the GUI threads are also used in order to not block other functions like navigation to other pages while the ball is for instance performing a pattern. 

2. One process for performing the image analysis. The camera is started and in each frame the ball is found if there is a ball to be found. The coordnates of the ball is then put in a queue for easy access from other processes. 

3. One process for using the a PID controller to find the a new wanted normalvector of the plate. The PID controller accesses the ball coordinates in the queue and performs calculations using previous known position and current position. From this process a packet och data containing x- and y-component of the normalvector, the height of the plateand four uint_8 for controlling leds and if a homingroutine is to be run. The leds are however not implemented and used, just prepared the packet. 

The script in the ESP32 is more simple and straight forward. It is implemented using two classes and a main script. One class contains the inverse kinematics of the table, which allows easy and fast conversion between the normal vector of the plate to three motor angles. The second class governs the control of the motors. Acceleration of motors and calculates the maximum speed of each motor. The motors are then moved to the positions found by inverse kinematics. This is the performed continuos in the main script and when a new packet is received the calculationn is performed again. 

## Common errors
When the robot is plugged in a terminal window is automatically opened to allow printing of error messages

#### Camera not found
1. Check if the camera is plugged in (USB behind the screen) and on top of camera arm. 
2. Try restarting the robot (plug it out and in)
3. Change camera index, line 11 in ```webcamera.py```

#### ESP not found
Use the command ```ls /dev/tty*``` to find the port, should be named ```/dev/ttyUSB#```
1. Check if the ESP is plugged in (USB behind the screen) and micro USB underneath the robot connected to the ESP. 
2. Change the range of USB ports, line 10 in ```communication.py```

#### Lost count of steps
This error is not printed in the terminal but can be seen. The error is can be visualized if no ball is on the robot but the plate is not horizontal. 

1. Press one of the three micro switches located under the arms. This will perform the homing routine and the robot will find its steps again. 
2. Restart the robot will have the same effect. 

#### Weird starting up procedure
Sometimes  when the robots is plugged in it do not start normally. It allows the user to choose operating system. If this is the case. 

1. Wait for the timer to run out. 
2. If 1. did not work. pluggit out and in and choose the Ubuntu operating system the next time. 

#### Computer want to update
If the computer sends a message that it wants to update, just press close or remind me later. 