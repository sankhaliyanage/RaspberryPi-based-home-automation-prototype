# RaspberryPi-based-home-automation-prototype
RaspberryPi based Home Automation using Input Output Analog and Digital Sensors
IOT assignment

[Related files]
- Part I
   - IOT_publisher.py
   - IOT_subscriber.py
- Part II
   - IOT_thingspeak.py
   - Thingspeak.com
	 - Access inforamtion
      - email : kimj179@unitec.ac.nz
	    - Id : kimj179
	    - Pw : Uniteckimj179
	    - Channel ID :   274555

[Part I - How to install and run files]

1. Testing kits which is used in our Assignment
   - GroviPi+
2. Install GrovePi+ library as below
   %git clone https://github.com/DexterInd/GrovePi.git
   %cd GrovePi/Script
   %sudo chmod +x install.sh
   %sudo ./install.sh
   %sudo reboot
3. Sensor connection on GrovePi+ test kits
   Sound Sensor : A0
   Light Sensor : A1
   Rotary Angle Sensor : A2
   Buzzer : D2
   Ultrasonic Sensor : D3
   Button : D4
   LED : D5
   Relay Sensor: D6
   Humidity and Temperature Sensor: D7
   LCD : any I2C port

4. Installation of the code
   Copy the code to any directory(example, /home/pi/work/)
   %cd /home/pi/work/
   %ls
    IOT_publisher.py  IOT_subscriber.py

5. How to run
  - Open terminal 1 and execute below code
     %python /home/pi/work/IOT_subscriber.py
     This code launches GUI frame to control subscription.
  - Open terminal 2 and execute below code
     %python /home/pi/work/IOT_publisher.py

6. Controls and output
  - Both python file output to consol about their activities.
  - IOT_subscriber launch GUI program
  - Steps
      -  Click "connect" button first to connect to server
      -  Click subscription button for each sensor
      -  GUI will display sensor data in red
      -  Click  "Display On" button will display sensor data on LCD.
      -  Subscription and Display button will be toggled.(sub <->unsub/display ON <->Off)

[Part II - Web Dashboard - Receiving data from Raspberry Pi]
1. Power on Raspberry Pi board with above configuration( Part I - 3)
2. Open terminal and run IOT_thingspeak.py file
   $python /home/pi/work/IOT_thingspeak.py
3. Find consol output
4. Open browser with below url
   https://thingspeak.com/
5. Log in with below information
  - email : kimj179@unitec.ac.nz
  - Id : kimj179
  - Pw : Uniteckimj179
  - Channel ID :   274555
6. Channel is already configured for our test environment.
  - 6 input field(Temp, Humidity,Proximity, sound, lght, rotary)
  - Go to "My Channels"
     From Home, menu -> Channel -> My Channel
  - Select "Unitec IOT assignment" Channel
  - Find 6 line graph for each input from sensors in test board.
7. Find all of charts are updated periodically with data from raspberry Pi.

[Part II - Web Dashboard - Send predefined command to Rasberry Pi]
1. Raspberry Pi is running with IOT_thingspeak.py
2. Go to "Talkback" menu
   From Home, menu -> Apps -> TalkBack
3. Select TalkBack named "Turn ON LCD and Backlight"
4. Select Add a new command button
5. Input command queue with one of below command(It is predefined in IOT_thingspeak.py file)
   TEMPUP, TEMPDOWN, RINGON, RINGOFF
7. Keep Reloading web brower(F5)
8. Find command is consumed(removed from command Queue)
9. Check Status of Rasberry Pi board
   Each command will drive actuator on test kits and display related information on LCD
10. After consuming all command, raspberry Pi just display "Hello Unitec" on LCD
11. Excepting predefined command, raspberry Pi display "Hello Unitec" message on LCD
