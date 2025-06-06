🔧 Assignment 4: Full-stack IoT System with ESP32, Flask, and Flet
🎯 Objective
Build an interactive application that monitors inputs and controls outputs on an ESP32 device. Your application should have:

frontend for user interaction.
backend as the API interface.
An ESP32 that connects .
You must include:

At least 2 input devices of your choice:1 digital (e.g., button, PIR motion sensor)
1 analog (e.g., potentiometer, LDR)
At least 2 output devices:1 digital (e.g., LED, relay)
1 analog (e.g., servo motor, PWM fan)

🧪 Scenario 2: Lab Safety Monitor
A lab safety assistant that warns when gas or dangerous presence is detected and logs sensor readings.

Inputs:
Potentiometer (analog): Detect air quality
Door magnetic sensor(Servo motor) (digital): Detect door open/closed
Outputs:
Buzzer (digital): Alarm
LED (analog): Indicate air quality level
Frontend:
Live sensor readings (gas %, door status)
Manual test alarm button
Log view of previous alerts

🧹 Technical Requirements
ESP32 communicates with Flask backend
Flet frontend must be interactive and fetch/send data via backend.
Include a schematic diagram or pin layout.
Well-commented code for ESP32, Flask, and Flet.
Use GitHub for version control (attach GitHub repository as part of your submission)

![image](https://github.com/user-attachments/assets/a04d38da-c5ac-4ab7-9cc4-6e24aa98a7c1)
