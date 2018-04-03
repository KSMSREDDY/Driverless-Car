import RPi.GPIO as GPIO                    #Import GPIO library
import time
import threading                                #Import time library


GPIO.setmode(GPIO.BOARD)                   #Set GPIO pin numbering

TRIG = 8                                  #Associate pin 23 to TRIG
ECHOF = 10                                 #Associate pin 24 to ECHO
ECHOR = 33
ECHOL = 37
mRA = 16
mRB = 18
mRE = 22
mLA = 11
mLB = 13
mLE = 15

print("Distance measurement in progress")

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHOF,GPIO.IN)                   #Set pin as GPIO in
GPIO.setup(ECHOR,GPIO.IN)
GPIO.setup(ECHOL,GPIO.IN)
GPIO.setup(mRA,GPIO.OUT)
GPIO.setup(mRB,GPIO.OUT)
GPIO.setup(mRE,GPIO.OUT)
GPIO.setup(mLA,GPIO.OUT)
GPIO.setup(mLB,GPIO.OUT)
GPIO.setup(mLE,GPIO.OUT)


def left_us():
    while GPIO.input(ECHOL)==0:               #Check whether the ECHO is LOW  
        pulse_startL = time.time()              #Saves the last known time of LOW
    while GPIO.input(ECHOL)==1:               #Check whether the ECHO is HIGH
        pulse_endL = time.time()                #Saves the last known time oR HIGH pulse 

    pulse_durationL = pulse_endL - pulse_startL #Get pulse duration to a variable
    distanceL = pulse_durationL * 17150        #Multiply pulse duration by 17150 to get distance
    distanceL = round(distanceL, 2)            #Round to two decimal points
    print("Left",distanceL,"cm")

def fwd_us():    
    while GPIO.input(ECHOF)==0:               #Check whether the ECHO is LOW  
        pulse_startF = time.time()              #Saves the last known time of LOW pulse
    while GPIO.input(ECHOF)==1:               #Check whether the ECHO is HIGH
        pulse_endF = time.time()                #Saves the last known time of HIGH pulse 

    pulse_durationF = pulse_endF - pulse_startF #Get pulse duration to a variable
    distanceF = pulse_durationF * 17150        #Multiply pulse duration by 17150 to get distance
    distanceF = round(distanceF, 2)            #Round to two decimal points
    print("Front",distanceF,"cm")

def right_us():
    while GPIO.input(ECHOR)==0:               #Check whether the ECHO is LOW  
        pulse_startR = time.time()             #Saves the last known time of LOW pulse
    while GPIO.input(ECHOR)==1:               #Check whether the ECHO is HIGH
        pulse_endR = time.time()               #Saves the last known time oR HIGH pulse 

    pulse_durationR = pulse_endR - pulse_startR #Get pulse duration to a variable
    distanceR = pulse_durationR * 17150        #Multiply pulse duration by 17150 to get distance
    distanceR = round(distanceR, 2)            #Round to two decimal points
    print("Right",distanceR,"cm")

  
    
    
    
try:

 while True:

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  print("Waiting For SensorF To Settle")
  time.sleep(1)                 
  
  tl = threading.Thread(target=left_us(),args=())
  tf = threading.Thread(target=fwd_us(),args=())
  tr = threading.Thread(target=right_us(),args=())
  
  tf.start()
  tl.start()
  tr.start()
  
  tf.join()
  tl.join()
  tr.join()
    
  
  if distanceF > 3 and distanceF < 30:      #Check whether the distance is within range
    print("Distance:",distanceF-0.5,"cm")   #Print distance with 0.5 cm calibration
    GPIO.output(mRA,GPIO.HIGH)
    GPIO.output(mRB,GPIO.LOW)
    GPIO.output(mRE,GPIO.HIGH)
    GPIO.output(mLA,GPIO.HIGH)
    GPIO.output(mLB,GPIO.LOW)
    GPIO.output(mLE,GPIO.HIGH)
    print('moving backward')
  elif distanceF >= 60 and distanceF < 90:      #Check whether the distance is within range
    print("Distance:",distanceF-0.5,"cm")   #Print distance with 0.5 cm calibration
    GPIO.output(mRA,GPIO.LOW)
    GPIO.output(mRB,GPIO.HIGH)
    GPIO.output(mRE,GPIO.HIGH)
    GPIO.output(mLA,GPIO.LOW)
    GPIO.output(mLB,GPIO.HIGH)
    GPIO.output(mLE,GPIO.HIGH)
    print('moving forward')  
  else:
    print("Distance:",distanceF-0.5,"cm")
    GPIO.output(mRE,GPIO.LOW)
    GPIO.output(mLE,GPIO.LOW)
    print("Stopped")                  #display out of range    
  
  
  
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Quit")
    

  

#def forward:
    
