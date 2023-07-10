from flask import Flask, jsonify, render_template
import RPi.GPIO as GPIO
import math
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time
from time import sleep
import pigpio

app = Flask(__name__)
app.config['DEBUG'] = True

factory = PiGPIOFactory()
pi = pigpio.pi()

s_curve_duration=1

def s_curve_position(current_time):
    t = current_time / s_curve_duration
    position = math.sin(math.pi/2 * t)  # You can adjust the formula as needed
    return position
 
#servo1 = Servo(17, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)     #pivot
servo1 = 17
servo2 = Servo(22, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)     #shoulder
servo3 = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)     #wrist
servo4 = Servo(24, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)     #rotate hand
servo5 = Servo(23, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)       #grip

dutycycle1 = -25           

servo1_min = 500
servo1_max = 2500

def set_servo_angle(angle):
    pulse_width = int(servo1_min + (servo1_max - servo1_min) * angle / 360.0)
    pi.set_servo_pulsewidth(servo1, pulse_width)
     
dutycycle2 = -44
dutycycle3 = -23
dutycycle4 = -5
dutycycle5 = -5

#servo1.value = math.sin(math.radians(dutycycle1))
servo2.value = math.sin(math.radians(dutycycle2))
servo3.value = math.sin(math.radians(dutycycle3))
servo4.value = math.sin(math.radians(dutycycle4))
servo5.value = math.sin(math.radians(dutycycle5))

pi.set_servo_pulsewidth(servo1, 1500)
time.sleep(0.2)
pi.set_servo_pulsewidth(servo1, 0)

GPIO.setmode(GPIO.BCM) 

#GPIO.setup(servo1, GPIO.OUT)
#GPIO.setup(servo2, GPIO.OUT)
#GPIO.setup(servo3, GPIO.OUT)
#GPIO.setup(servo4, GPIO.OUT)
#GPIO.setup(grip, GPIO.OUT)

#p1 = GPIO.PWM(servo1, 50)
#p2 = GPIO.PWM(servo2, 50)
#p3 = GPIO.PWM(servo3, 50)
#p4 = GPIO.PWM(servo4, 50)
#p5 = GPIO.PWM(grip, 50)

#p1.start(0)
#p2.start(0)
#p3.start(0)
#p4.start(0)
#p5.start(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_dutycycle1')
def get_dutycycle1():
    global dutycycle1
    return jsonify({'dutycycle1': dutycycle1})

@app.route('/get_dutycycle2')
def get_dutycycle2():
    global dutycycle2
    return jsonify({'dutycycle2': dutycycle2})

@app.route('/get_dutycycle3')
def get_dutycycle3():
    global dutycycle3
    return jsonify({'dutycycle3': dutycycle3})

@app.route('/get_dutycycle4')
def get_dutycycle4():
    global dutycycle4
    return jsonify({'dutycycle4': dutycycle4})

@app.route('/get_grip')
def get_dutycycle5():
    global dutycycle5
    return jsonify({'dutycycle5': dutycycle5})

@app.route('/increment_dutycycle1', methods=['POST'])
def increment_dutycycle1():
    pi.set_servo_pulsewidth(servo1, 1800)
    time.sleep(0.2)
    pi.set_servo_pulsewidth(servo1, 0)
    sleep(1)
    #p1.ChangeDutyCycle(0)
    return jsonify({'dutycycle1': dutycycle1})

@app.route('/increment_dutycycle2', methods=['POST'])
def increment_dutycycle2():
    global dutycycle2
    #dutycycle2 += 0.5
    #p2.ChangeDutyCycle(float(dutycycle2))
    min_angle = dutycycle2
    max_angle = dutycycle2 + 2
    start_time = time.time()
    flag=1

    while True:
        current_time = time.time() - start_time

        if current_time >= s_curve_duration:
            break

        position = s_curve_position(current_time)
        angle = min_angle + (max_angle - min_angle) * position
        #print(angle)
        if(angle<10):
            servo2.value = math.sin(math.radians(angle))
            sleep(0.01)
        else:
            flag=0
            break
    print(flag)
    if(flag):
        dutycycle2+=2
    sleep(1)
    #p2.ChangeDutyCycle(0)
    return jsonify({'dutycycle2': dutycycle2})

@app.route('/increment_dutycycle3', methods=['POST'])
def increment_dutycycle3():
    global dutycycle3
    #dutycycle3 += 0.5
    #p3.ChangeDutyCycle(float(dutycycle3))
    min_angle = dutycycle3
    max_angle = dutycycle3 + 2
    start_time = time.time()
    flag=1

    while True:
        current_time = time.time() - start_time

        if current_time >= s_curve_duration:
            break

        position = s_curve_position(current_time)
        angle = min_angle + (max_angle - min_angle) * position
        #print(angle)
        if(angle<17):
            servo3.value = math.sin(math.radians(angle))
            sleep(0.01)
        else:
            flag=0
            break
    print(flag)
    if(flag):
        dutycycle3+=2
    sleep(1)
    #sleep(1)
    #p3.ChangeDutyCycle(0)
    return jsonify({'dutycycle3': dutycycle3})

@app.route('/increment_dutycycle4', methods=['POST'])
def increment_dutycycle4():
    global dutycycle4
    #dutycycle4 += 0.5
    #p4.ChangeDutyCycle(float(dutycycle4))
    min_angle = dutycycle4
    max_angle = dutycycle4 + 5
    start_time = time.time()
    flag=1

    while True:
        current_time = time.time() - start_time

        if current_time >= s_curve_duration:
            break

        position = s_curve_position(current_time)
        angle = min_angle + (max_angle - min_angle) * position
        #print(angle)
        if(angle<40):
            servo4.value = math.sin(math.radians(angle))
            sleep(0.01)
        else:
            flag=0
            break
    print(flag)
    if(flag):
        dutycycle4+=5
    sleep(1)
    #sleep(1)
    #p4.ChangeDutyCycle(0)
    return jsonify({'dutycycle4': dutycycle4})

@app.route('/grip', methods=['POST'])
def grip():
    global dutycycle5
    #dutycycle5 += 5
    #p5.ChangeDutyCycle(float(dutycycle5))
    min_angle = dutycycle5
    max_angle = dutycycle5 + 3.5
    start_time = time.time()
    flag=1

    while True:
        current_time = time.time() - start_time

        if current_time >= s_curve_duration:
            break

        position = s_curve_position(current_time)
        angle = min_angle + (max_angle - min_angle) * position
        #print(angle)
        if(angle<5):
            servo5.value = math.sin(math.radians(angle))
            sleep(0.01)
        else:
            flag=0
            break
    print(flag)
    if(flag):
        dutycycle5+=3.5
    sleep(1)
    #sleep(1)
    #p5.ChangeDutyCycle(0)
    return jsonify({'dutycycle5': dutycycle5})

@app.route('/decrement_dutycycle1', methods=['POST'])
def decrement_dutycycle1():
    pi.set_servo_pulsewidth(servo1, 1200)
    time.sleep(0.2)
    pi.set_servo_pulsewidth(servo1, 0)
    sleep(1)
    #p1.ChangeDutyCycle(0)
    return jsonify({'dutycycle1': dutycycle1})

@app.route('/decrement_dutycycle2', methods=['POST'])
def decrement_dutycycle2():
    global dutycycle2
    if(dutycycle2>-44):
        #dutycycle2 -= 0.5
        #p2.ChangeDutyCycle(float(dutycycle2))
        #sleep(1)
        #p2.ChangeDutyCycle(0)
        min_angle = dutycycle2 - 2
        max_angle = dutycycle2 
        start_time = time.time()

        while True:
            current_time = time.time() - start_time

            if current_time >= s_curve_duration:
                break

            position = s_curve_position(current_time)
            angle = max_angle - (max_angle - min_angle) * position
            servo2.value = math.sin(math.radians(angle))
            sleep(0.01)
        dutycycle2-=2
        sleep(1)
    return jsonify({'dutycycle2': dutycycle2})

@app.route('/decrement_dutycycle3', methods=['POST'])
def decrement_dutycycle3():
    global dutycycle3
    if(dutycycle3>-83):
        #dutycycle3 -= 0.5
        #p3.ChangeDutyCycle(float(dutycycle3))
        #sleep(1)
        #p3.ChangeDutyCycle(0)
        min_angle = dutycycle3 - 2
        max_angle = dutycycle3 
        start_time = time.time()

        while True:
            current_time = time.time() - start_time

            if current_time >= s_curve_duration:
                break

            position = s_curve_position(current_time)
            angle = max_angle - (max_angle - min_angle) * position
            servo3.value = math.sin(math.radians(angle))
            sleep(0.01)
        dutycycle3-=2
        sleep(1)
    return jsonify({'dutycycle3': dutycycle3})

@app.route('/decrement_dutycycle4', methods=['POST'])
def decrement_dutycycle4():
    global dutycycle4
    if(dutycycle4>-40):
        #dutycycle4 -= 0.5
        #p4.ChangeDutyCycle(float(dutycycle4))
        #sleep(1)
        #p4.ChangeDutyCycle(0)
        min_angle = dutycycle4 - 5
        max_angle = dutycycle4 
        start_time = time.time()

        while True:
            current_time = time.time() - start_time

            if current_time >= s_curve_duration:
                break

            position = s_curve_position(current_time)
            angle = max_angle - (max_angle - min_angle) * position
            servo4.value = math.sin(math.radians(angle))
            sleep(0.01)
        dutycycle4-=5
        sleep(1)
    return jsonify({'dutycycle4': dutycycle4})

@app.route('/release', methods=['POST'])
def release():
    global dutycycle5
    if(dutycycle5>-40):
        #dutycycle5 -= 5
        #p5.ChangeDutyCycle(float(dutycycle5))
        #sleep(1)
        #p5.ChangeDutyCycle(0)
        min_angle = dutycycle5 - 3.5
        max_angle = dutycycle5 
        start_time = time.time()

        while True:
            current_time = time.time() - start_time

            if current_time >= s_curve_duration:
                break

            position = s_curve_position(current_time)
            angle = max_angle - (max_angle - min_angle) * position
            servo5.value = math.sin(math.radians(angle))
            sleep(0.01)
        dutycycle5-=3.5
        sleep(1)
    return jsonify({'dutycycle5': dutycycle5})

if _name_ == '_main_':
    app.run()