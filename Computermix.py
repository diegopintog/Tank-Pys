#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import curses
import os

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

#Definition of  motor pin 
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#Definition of base speeds
SPEED_LOW  = 25
SPEED_HIGH = 50
SPEED_BRAKE = 10

#Set the GPIO port to BCM encoding mode
GPIO.setmode(GPIO.BCM)

#Ignore warning information
GPIO.setwarnings(False)

#Motor pin initialization operation
def motor_init():
    global pwm_ENA
    global pwm_ENB
    global delaytime
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #Set the PWM pin and frequency is 2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)


#advance
def run():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_LOW)
    pwm_ENB.ChangeDutyCycle(SPEED_LOW)
    

#back
def back():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(SPEED_LOW)
    pwm_ENB.ChangeDutyCycle(SPEED_LOW)
    

#turn left
def left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_LOW)
    pwm_ENB.ChangeDutyCycle(SPEED_HIGH)
    

#turn right
def right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_HIGH)
    pwm_ENB.ChangeDutyCycle(SPEED_LOW)
    

#turn left in place
def spin_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_HIGH)
    pwm_ENB.ChangeDutyCycle(SPEED_HIGH)
   

#turn right in place
def spin_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(SPEED_HIGH)
    pwm_ENB.ChangeDutyCycle(SPEED_HIGH)
    
#back to the right
def back_to_right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_HIGH)
    pwm_ENB.ChangeDutyCycle(SPEED_HIGH)
    

#brake
def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(SPEED_BRAKE)
    pwm_ENB.ChangeDutyCycle(SPEED_BRAKE)

# Speed up by 10
def speed_up():
    SPEED_LOW = SPEED_LOW + 10
    SPEED_HIGH = SPEED_HIGH + 10
    run()

# Slow down by 10
def speed_down():
    SPEED_LOW = SPEED_LOW - 10
    SPEED_HIGH = SPEED_HIGH - 10
    run()
       
try:
    motor_init()
    while True:
        char = screen.getch()
        if char == ord('w'):
            run()
        elif char == ord('s'):
            back()
        elif back() and char == ord('a'):
            back_to_right()
        elif char == ord('a'):
            left()
        elif char == ord('d'):
            right()
        elif char == ord('q'):
            spin_left()
        elif char == ord('e'):
            spin_right()
        elif char == ord('x'):
            brake()
        elif char == ord('t'):
            speed_up()
        elif char == ord('g'):
            speed_down()
        elif char == ord('1'):
            pwm_ENA.ChangeDutyCycle(SPEED_BRAKE)
            pwm_ENB.ChangeDutyCycle(SPEED_BRAKE)
        elif char == ord('2'):
            pwm_ENA.ChangeDutyCycle(SPEED_BRAKE * 2)
            pwm_ENB.ChangeDutyCycle(SPEED_BRAKE * 2)
        elif char == ord('5'):
            pwm_ENA.ChangeDutyCycle(SPEED_HIGH)
            pwm_ENB.ChangeDutyCycle(SPEED_HIGH)    
            



finally:
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    GPIO.cleanup()
    pwm_ENA.stop()
    pwm_ENB.stop()
    GPIO.cleanup()
