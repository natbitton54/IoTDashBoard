# IoTDashBoard
IoT Course Final Project

This project is using the flask framework so the need to install flask in rpi is a must

to install flask:

1. Open your terminal
2. run the command: sudo apt install python3-flask

This is if you don't have flask on your RPi but most likely, you already have it.
----------------------------------------------------------------------------------------
How to run this project

to run:

1. Press run on VS Code or whatever IDE you're using.
2. On your browser, go to http://127.0.0.1:5000.

http://127.0.0.1:5000 is the local development server URL of flask where:
127.0.0.1 is the localhost
5000 is the default port
----------------------------------------------------------------------------------------
In some part of trying to run the code, you might encounter an error on your gpio.

to fix this:

1. Open your terminal
2. run the command: sudo apt install python3-rpi.gpio

This probably means that you don't have the required version of gpio.