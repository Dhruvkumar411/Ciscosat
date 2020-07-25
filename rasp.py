import urllib
import RPi.GPIO as GPIO
import time
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setup(07,GPIO.OUT)
oGPIO_TRIGGER = 11
oGPIO_ECHO = 13
GPIO_TRIGGER = 12
GPIO_ECHO = 18 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(oGPIO_TRIGGER, GPIO.OUT)
GPIO.setup(oGPIO_ECHO, GPIO.IN)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = 0
    StopTime = 0
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 #########
    # set Trigger to HIGH
def oDistance():
    GPIO.output(oGPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(oGPIO_TRIGGER, False)

    oStartTime = 0
    oStopTime = 0

    while GPIO.input(oGPIO_ECHO) == 0:
        oStartTime = time.time()
    while GPIO.input(oGPIO_ECHO) == 1:
        oStopTime = time.time()

  # time difference between start and arrival
    oTimeElapsed = oStopTime - oStartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    odistance = (oTimeElapsed * 34300) / 2
    return odistance
pwm=GPIO.PWM(07,50)
pwm.start(0) 
val_ue=0
#change into percentage
def perc(val_ue):
	perc_value=(val_ue/18)*100
	if perc_value > 100:
		perc_value=100
	elif perc_value < 0:
		perc_value=0
	pe=100-perc_value
	return pe
def SetAngle(angle):
	#pwm.start(0)
	duty = angle / 18 + 2
	GPIO.output(07,True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(07,False)
	pwm.ChangeDutyCycle(0)
	#pwm.stop()

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
	    per_val=perc(dist)
	    upload_value=per_val;
           # data = urllib.urlopen("https://api.thingspeak.com/update?api_key=468LT8FC7Q11FXC5&field1=h"+str(upload_value));
	    odist = oDistance()
            print ("Measured Distance = %.1f " % per_val)
	   # print ("Measured Distance outside = %.1f cm" % odist)
	    if odist >= 20:
               SetAngle(0)
            else:
	       SetAngle(90) 
	    if per_val  >= 75:
		GPIO.output(40,False)
		GPIO.output(38,False)
		GPIO.output(36,True)
		print ("okay")
	    elif (per_val >= 50):
		GPIO.output(36,False)
		GPIO.output(38,True)
		GPIO.output(40,False)
		print ("more than half")
	    else:
		GPIO.output(36,False)
		GPIO.output(38,False)
		GPIO.output(40,True)
		print ("full unload urgently")
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
