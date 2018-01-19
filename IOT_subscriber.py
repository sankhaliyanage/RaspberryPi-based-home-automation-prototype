'''
Revision history
 2017-05-17    Initial draft for GUI
 2017-05-18    Toggle buttons

'''
from Tkinter import *
import paho.mqtt.client as mqtt
from threading import Timer
import time
from signal import pause
import ttk
from  grovepi import *
import math
from grove_rgb_lcd import *

##### MQTT server configuration
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
	print("connected with result code "+str(rc))
	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	###   client.subscribe("myTopic")  --> this call move to button's action handler

'''
client.publish("rotary_sensor", str(rotary_sensor_value), 0)
client.publish("button_sensor", str(button_status), 0)
client.publish("ultrasonic_sensor", str(distant), 0)
client.publish("humidity_sensor", str(hum), 0)
client.publish("temperature_sensor", str(temp), 0)
client.publish("light_sensor", str(light_intensity), 0)
client.publish("sound_sensor", str(sound_level), 0)
'''
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # message handler for each sensor
    # set incoming messages from server
    if msg.topic=="rotary_sensor":
        rotary.set(msg.payload)
    elif msg.topic=="button_sensor":
        button.set(msg.payload)
    elif msg.topic=="ultrasonic_sensor":
        ultrasonic.set(msg.payload)
    elif msg.topic=="humidity_sensor":
        humidity.set(msg.payload)
    elif msg.topic=="temperature_sensor":
        temperature.set(msg.payload)
    elif msg.topic=="light_sensor":
        light.set(msg.payload)
    elif msg.topic=="sound_sensor":
        sound.set(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


##### GUI framework #####
root = Tk()
frame = Frame(root)
frame.pack()
root.title('IOT Assignment-Subscription, Unitec')

# layout frame and button
'''
#Buttons
Toggle Subscribe/Unsubscribe button for each sensors(rotary, button, ultrasonic, humidity, temperature, light, sound)
Toggle Display On/Off button for each sensors(rotary, button, ultrasonic, humidity, temperature, light, sound)
Connect / Disconnect
'''
# sensor value from mqtt server
rotary = StringVar()
button = StringVar()
ultrasonic = StringVar()
humidity = StringVar()
temperature = StringVar()
light = StringVar()
sound = StringVar()

#display_index = 0 # initial state = OFF
# button handler
# rotary
def subscribe_rotary():
    if t_rbtn.config('text')[-1] == 'Subscribe Rotary':
        print("Subscribe rotary sensor")
        client.subscribe("rotary_sensor")
        t_rbtn.config(text='Unsubscribe Rotary')
    else:
        print("Unsubscribe rotary sensor")
        client.unsubscribe("rotary_sensor")
        rotary.set("N/A")
        t_rbtn.config(text='Subscribe Rotary')

def display_rotary():
    if t_rdbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(255,0,0)
        setText("rotary :" + rotary.get())
        t_rdbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_rdbtn.config(text='Display ON')

# button
def subscribe_button():
    if t_bbtn.config('text')[-1] == 'Subscribe button':
        print("Subscribe button sensor")
        client.subscribe("button_sensor")
        t_bbtn.config(text='Unsubscribe button')
    else:
        print("Unsubscribe button sensor")
        client.unsubscribe("button_sensor")
        button.set("N/A")
        t_bbtn.config(text='Subscribe button')

def display_button():
    if t_bdbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(0,255,0)
        setText("button :" + button.get())
        t_bdbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_bdbtn.config(text='Display ON')


# ultrasonic
def subscribe_ultrasonic():
    if t_ubtn.config('text')[-1] == 'Subscribe ultrasonic':
        print("Subscribe ultrasonic sensor")
        client.subscribe("ultrasonic_sensor")
        t_ubtn.config(text='Unsubscribe ultrasonic')
    else:
        print("Unsubscribe ultrasonic sensor")
        client.unsubscribe("ultrasonic_sensor")
        ultrasonic.set("N/A")
        t_ubtn.config(text='Subscribe ultrasonic')

def display_ultrasonic():
    if t_udbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(125, 125,0)
        setText("ultrasonic :" + ultrasonic.get())
        t_udbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_udbtn.config(text='Display ON')

# Humidity
def subscribe_humidity():
    if t_hbtn.config('text')[-1] == 'Subscribe humidity':
        print("Subscribe humidity sensor")
        client.subscribe("humidity_sensor")
        t_hbtn.config(text='Unsubscribe humidity')
    else:
        print("Unsubscribe humidity sensor")
        client.unsubscribe("humidity_sensor")
        humidity.set("N/A")
        t_hbtn.config(text='Subscribe humidity')

def display_humidity():
    if t_hdbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(125,0,125)
        setText("humidity :" + humidity.get()+ "%")
        t_hdbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_hdbtn.config(text='Display ON')

# temperature
def subscribe_temperature():
    if t_tbtn.config('text')[-1] == 'Subscribe temperature':
        print("Subscribe temperature sensor")
        client.subscribe("temperature_sensor")
        t_tbtn.config(text='Unsubscribe temperature')
    else:
        print("Unsubscribe temperature sensor")
        client.unsubscribe("temperature_sensor")
        temperature.set("N/A")
        t_tbtn.config(text='Subscribe temperature')

def display_temperature():
    if t_tdbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(0,125,125)
        setText("temperature :" + temperature.get()+ "C")
        t_tdbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_tdbtn.config(text='Display ON')

# light
def subscribe_light():
    if t_lbtn.config('text')[-1] == 'Subscribe light':
        print("Subscribe light sensor")
        client.subscribe("light_sensor")
        t_lbtn.config(text='Unsubscribe light')
    else:
        print("Unsubscribe light sensor")
        client.unsubscribe("light_sensor")
        light.set("N/A")
        t_lbtn.config(text='Subscribe light')

def display_light():
    if t_ldbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(0,0,255)
        setText("light :" + light.get() )
        t_ldbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_ldbtn.config(text='Display ON')

# sound
def subscribe_sound():
    if t_sbtn.config('text')[-1] == 'Subscribe sound':
        print("Subscribe sound sensor")
        client.subscribe("sound_sensor")
        t_sbtn.config(text='Unsubscribe sound')
    else:
        print("Unsubscribe sound sensor")
        client.unsubscribe("sound_sensor")
        sound.set("N/A")
        t_sbtn.config(text='Subscribe sound')

def display_sound():
    if t_sdbtn.config('text')[-1] =='Display ON':
        print("Turn ON the LCD")
        setRGB(0, 255, 255)
        setText("sound :" + sound.get() )
        t_sdbtn.config(text='Display OFF')
    else:
        print("Turn OFF the LCD")
        setRGB(0,0,0)
        setText(" ")
        t_sdbtn.config(text='Display ON')


# connect/disconnected
def connect():
    print("Connected to server")
    client.username_pw_set("user40", password="xWnuPCYe")
    client.connect("202.50.209.80", 1883, 60)
    client.loop_start()

def disconnect():
    print("Disconnected to server")
    client.disconnect()
    client.loop_stop()

def exit():
    print("Exiting... Bye")
    client.disconnect()
    client.loop_stop()
    root.destroy()

row_num = 0 # line number
button_width = 20
#label-rotary
Label(frame,text='Rotary', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = rotary, width=button_width, fg = "red").grid(row=row_num,column=1)
t_rbtn=Button(frame,text='Subscribe Rotary',command=subscribe_rotary, width=button_width)
t_rbtn.grid(row=row_num,column=2)
t_rdbtn=Button(frame,text='Display ON',command=display_rotary, width=button_width)
t_rdbtn.grid(row=row_num,column=3)

#label-button
row_num = row_num + 1
Label(frame,text='button', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = button, width=button_width, fg = "red").grid(row=row_num,column=1)
t_bbtn=Button(frame,text='Subscribe button',command=subscribe_button, width=button_width)
t_bbtn.grid(row=row_num,column=2)
t_bdbtn=Button(frame,text='Display ON',command=display_button, width=button_width)
t_bdbtn.grid(row=row_num,column=3)

#label-ultrasonic
row_num = row_num + 1
Label(frame,text='ultrasonic', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = ultrasonic, width=button_width, fg = "red").grid(row=row_num,column=1)
t_ubtn=Button(frame,text='Subscribe ultrasonic',command=subscribe_ultrasonic, width=button_width)
t_ubtn.grid(row=row_num,column=2)
t_udbtn=Button(frame,text='Display ON',command=display_ultrasonic, width=button_width)
t_udbtn.grid(row=row_num,column=3)

#label-humidity
row_num = row_num + 1
Label(frame,text='humidity', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = humidity, width=button_width, fg = "red").grid(row=row_num,column=1)
t_hbtn=Button(frame,text='Subscribe humidity',command=subscribe_humidity, width=button_width)
t_hbtn.grid(row=row_num,column=2)
t_hdbtn=Button(frame,text='Display ON',command=display_humidity, width=button_width)
t_hdbtn.grid(row=row_num,column=3)

#label-temperature
row_num = row_num + 1
Label(frame,text='temperature', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = temperature, width=button_width, fg = "red").grid(row=row_num,column=1)
t_tbtn=Button(frame,text='Subscribe temperature',command=subscribe_temperature, width=button_width)
t_tbtn.grid(row=row_num,column=2)
t_tdbtn=Button(frame,text='Display ON',command=display_temperature, width=button_width)
t_tdbtn.grid(row=row_num,column=3)

#label-light
row_num = row_num + 1
Label(frame,text='light', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = light, width=button_width, fg = "red").grid(row=row_num,column=1)
t_lbtn=Button(frame,text='Subscribe light',command=subscribe_light, width=button_width)
t_lbtn.grid(row=row_num,column=2)
t_ldbtn=Button(frame,text='Display ON',command=display_light, width=button_width)
t_ldbtn.grid(row=row_num,column=3)

#label-sound
row_num = row_num + 1
Label(frame,text='sound', width=button_width).grid(row=row_num,column=0)
Label(frame,textvariable = sound, width=button_width, fg = "red").grid(row=row_num,column=1)
t_sbtn=Button(frame,text='Subscribe sound',command=subscribe_sound, width=button_width)
t_sbtn.grid(row=row_num,column=2)
t_sdbtn=Button(frame,text='Display ON',command=display_sound, width=button_width)
t_sdbtn.grid(row=row_num,column=3)

#label-Connect/Disconnect
row_num = row_num + 1
Button(frame,text='Connect',command=connect, width=button_width).grid(row=row_num,column=0)
Button(frame,text='Disconnect',command=disconnect, width=button_width).grid(row=row_num,column=1)
Button(frame,text='Exit', command=exit, width=button_width).grid(row=row_num,column=3)

root.mainloop()
