
import httplib, urllib
import time
from  grovepi import *
from grove_rgb_lcd import *

WKEY = '57U9CEIXT2WF00PC'
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
DEBUG = True

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

# TaklBack Definition
# ThingsSpeak -> Apps -> TalkBack
TalkBackID = '15763'
TalkBackAPIKey = 'X0TF1DGNJFOY2G6W'


loop_cnt = 0
while True:
    time.sleep(1)
    loop_cnt = loop_cnt+1
    print '===========>>> Loop count  = ', loop_cnt
    # read temp sensor, field 1 and field 2
    [temp, hum] = dht(dht_sensor_port,0)
    print("Temp : ",temp, "C    Humidity : ", hum, "%")
    time.sleep(1)

    # read proximity sensor, field 3
    distant = ultrasonicRead(ultrasonic_ranger_port)
    print("Distance : ", distant)
    time.sleep(1)

    # read sound sensor, field 4
    sound = analogRead(sound_sensor_port)
    print("Sound level : " , sound)
    time.sleep(1)

    # read light sensor, field 5
    light = analogRead(light_sensor_port)
    print("Light level : ", light )
    time.sleep(1)

    # read rotary sensor, field 6
    rotary = analogRead(rotary_sensor_port)
    print("Rotary button value : ", rotary)
    time.sleep(1)



    params = urllib.urlencode({"field1": temp,"field2": hum, "field3":distant, "field4":sound, "field5":light, "field6":rotary,  "key": WKEY})
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print ("Status :", response.status,"Reason:", response.reason)
        data = response.read()
        conn.close()

    except KeyboardInterrupt:
        print("Key interrupt occured")
        break

    except:
        print "Connection failed"

    #  Execute Next TalkBack Command
    #  From https://au.mathworks.com/help/thingspeak/talkback-app.html#execute_talkback_comand
    #  POST https://api.thingspeak.com/talkbacks/TALKBACK_ID/commands/execute
    #       api_key=YOUR_TALKBACK_API_KEY
    #  Response is command string. Ex. OPENDOOR
    talkBackURL =  "http://api.thingspeak.com/talkbacks/" + TalkBackID + "/commands/execute?api_key=" + TalkBackAPIKey;

    # Request command to thingspeak server( dispatch a single command from commend buffer )
    command = conn.request("GET", talkBackURL)
    command = conn.getresponse()
    action = command.read()
    print 'COMMAND: ',action

    # Predefined command for Raspberry Pi
    # All of actions performed display on LCD
    #   COMMAND         ACTION
    # 1. TEMPUP        Turn on Relay(HEATER)
    # 2. TEMPDOWN      Turn off Relay(HEATER)
    # 3. RINGON        Ring on Buzzer
    # 4. RINGOFF       Ring off Buzzer

    if action == "TEMPUP":
        print 'Requesting...Turn on Heater'
        print("CurrentTemp:"+str(temp)+"C")
        #turn on Heater - relay sensor ON
        digitalWrite(relay_port,1)
        #display the action on LCD
        setRGB(255, 0, 0)
        setText("CurrentTemp:" + str(temp) + "C"+" Heater is ON")
    elif action == "TEMPDOWN":
        print 'Requesting...Turn off Heater'
        print("CurrentTemp:"+str(temp)+"C")
        #turn off Heater - relay sensor OFF
        digitalWrite(relay_port,0)
        #display the action on LCD
        setRGB(0, 0, 255)
        setText("CurrentTemp:" + str(temp) + "C"+" Heater is Off")
    elif action =="RINGON":
        print 'Requesting... Turn On Alarm'
        #turn on Alarm - Buzzer is On
        digitalWrite(buzzer_port,1)
        #display the action on LCD
        setRGB(255, 0, 0)
        setText("Warning...Alarm turned On")
    elif action == "RINGOFF":
        print 'Requesting... Turn Off Alarm'
        #turn off Alarm - Buzzer is Off
        digitalWrite(buzzer_port,0)
        #display the action on LCD
        setRGB(0, 255, 0)
        setText("Cleared...Turning Off Alarm")
    else:
        print 'NO command available or invalid command'
        #turn off all sensors
        digitalWrite(relay_port,0)
        digitalWrite(buzzer_port,0)
        setRGB(255, 255, 0)
        setText("Hello Unitec!! Testing is finished!! Bye")
        time.sleep(2)
        setRGB(0,0,0)




        
