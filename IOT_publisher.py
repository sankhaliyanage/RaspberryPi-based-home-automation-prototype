'''
Revision history
 2017-05-16    Initial draft for driving sensors
 2017-05-17    Add MQTT function
               Subscription to Unitec server

'''
import time
from  grovepi import *
import math
# for LCD
from grove_rgb_lcd import *
# for MQTT server
import paho.mqtt.client as mqtt
import datetime

# Debug Feature
DEBUG = False

'''
Sensors
Digital-input Sensors
- Button
- Ultrasonic
- Humididity and Temperature

Digital-output Sensors
- Buzzer
- LED ( analog-PWM data and digital output)
- Relay

Analog-input Sensors
- rotary
- Light

Analog-output Sensors
- Sound

I2C device
- LCD
'''


##### Definition of Sensor connection for ANALOG PORT #####
# Sound Sensor :Analog A0
sound_sensor_port = 0
# Light Sensor :Analog A1
light_sensor_port = 1
# Rotary Angle Sensor :Analog A2
rotary_sensor_port = 2



##### Definition of Sensor connection for DIGITAL PORT #####
##### Assign PIN mode #####
# Buzzer - D2
buzzer_port = 2
pinMode(buzzer_port,"OUTPUT")	# Assign mode for buzzer as output

# Ultrasonic Sensor - D3
# read by ultrasonicRead()
ultrasonic_ranger_port = 3

# Button - D4
button_port = 4
pinMode(button_port,"INPUT")		# Assign mode for Button as input

# LED : Digital D5
led_port = 5
pinMode(led_port,"OUTPUT")

# Relay Sensor
relay_port = 6
pinMode(relay_port,"OUTPUT")

# Humidity and Temperature Sensor
# ready by dht() function
dht_sensor_port = 7

##### I2C device #####
# LCD on any I2C port


##### MQTT server setting #####
def on_connect(client, userdata, rc):
    print("connected with result code"+str(rc))

def on_publish(client, packet, mid):
    print("published")

def on_disconnect(client, userdata, rc):
    print("disconnected")

# mqtt
client=mqtt.Client()
client.username_pw_set("user40", password="xWnuPCYe")
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnnect = on_disconnect
client.connect("202.50.209.80", 1883, 60)

'''
# Publication
client.publish("rotary_sensor", str(rotary_sensor_value), 0)
client.publish("button_sensor", str(button_status), 0)
client.publish("ultrasonic_sensor", str(distant), 0)
client.publish("humidity_sensor", str(hum), 0)
client.publish("temperature_sensor", str(temp), 0)
client.publish("light_sensor", str(light_intensity), 0)
client.publish("sound_sensor", str(sound_level), 0)

'''
##### end of MQTT settings #####

# Initial values
rotary_sensor_value = -1
loop_count = 0
button_status = 0
distant = -1
temp = -1
hum = -1

# interval between sensor controls
pause = 0.5 # secs

while True:
    client.publish("myTopic", "This is groupwork of IOT, JinTaeKim, Sankha, Ovini and Manoj", 0)
    loop_count = loop_count + 1
    print(str(datetime.datetime.now())," ################# Loop count : #################",loop_count)

    try:
        ##### Action for each sensor #####
        ##### Input Sensors  #####
        # 1. Rotary sensor - Read resistance from Potentiometer - Rotary sensor
        if loop_count%1 == 0:
            rotary_sensor_value = analogRead(rotary_sensor_port)
            print("1. rotary sensor :",rotary_sensor_value)
            # Publish rotary sensor data
            client.publish("rotary_sensor", str(rotary_sensor_value), 0)
            time.sleep(pause)

        # 2. Read Button sensor
        if loop_count%2 == 0:
            button_status = digitalRead(button_port)
            print("2. Button status :",button_status)
            # Publish button sensor data
            client.publish("button_sensor", str(button_status), 0)
            time.sleep(pause)

        # 3. Read distance value from Ultrasonic
        if loop_count%3 == 0:
            distant = ultrasonicRead(ultrasonic_ranger_port)
            print("3. Untrasonic sensor", distant,'cm')
            # Publish untrasonic sensor data
            client.publish("ultrasonic_sensor", str(distant), 0)
            time.sleep(pause)

        # 4, 5 Read Humidity and Temperature
        # Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
        #  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
        #  1 - DHT22 - white one, aka DHT Pro or AM2302
        #  2 - DHT21 - black one, aka AM2301
        if loop_count%4 == 0:
            [ temp,hum ] = dht(dht_sensor_port,0)
            print("4. Temp =", temp, "C")
            # Publish Humidity sensor data
            client.publish("humidity_sensor", str(hum), 0)
            time.sleep(pause)
            print("5. Humidity=", hum,"%")
            # Publish Temperature sensor data
            client.publish("temperature_sensor", str(temp), 0)
            time.sleep(pause)

        # 6. Read light_sensor_port
        if loop_count%5 == 0:
            light_intensity = analogRead(light_sensor_port)
            print("6. light level :", light_intensity)
            # Publish Light sensor data
            client.publish("light_sensor", str(light_intensity), 0)
            time.sleep(pause)

        # 7. Read sound_sensor_port
        if loop_count%6 == 0:
            sound_level = analogRead(sound_sensor_port)
            print("7. sound level :", sound_level)
            # Publish Sound sensor data
            client.publish("sound_sensor", str(sound_level), 0)
            time.sleep(pause)


        ##### Output Sensors ####
        if DEBUG :
            # 1. LED - Send PWM signal to LED
            # NEED TO CHECK : LED CAN BE USED BY digitalWrite - On/Off
            analogWrite(led_port,rotary_sensor_value//4)
            print("Wrinting LED")

            # 2. Buzzer - Buzzing based on value of input-2, Button Sensor
            if button_status:	#If the Button is in HIGH position, run the program
                digitalWrite(buzzer_port,1)
                print("Buzzer ON")
                # print "\tBuzzing"
            else:		#If Button is in Off position, print "Off" on the screen
                digitalWrite(buzzer_port,0)
                print("Buzzer OFF")
                # print "Off"

            # 3. Relay sensor - output based on value from Ultrasonic sensor
            if distant <= 10:
                digitalWrite(relay_port,1)
                print("Distance is less then 10cm")
            else:
                digitalWrite(relay_port,0)
                print("Distance is Greater then 10cm")

            # 4. Output temperature and Humidity to LCD on I2C port
            t = str(temp)   # "stringify" the display values
            h = str(hum)
            setRGB(255, 0, 0)
            time.sleep(pause)
            setRGB(0, 255, 0)
            time.sleep(pause)
            setRGB(0, 0, 255)
            setText("Temp:" + t + "C      " + "Humidity :" + h + "%") # update the RGB LCD display
            print("Temp:"+t+"C    "+"Humidity:" + h + "%")

    except KeyboardInterrupt:
        print("Key interrupt occured")
        break

    except IOError:
        print("Error")
