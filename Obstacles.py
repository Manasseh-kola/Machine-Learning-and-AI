import RPi.GPIO as GPIO
import os
import time
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24


def obstacle_detection():
  
    print ("Measuring Distance")
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    
    try:
        while True:
    
            GPIO.output(TRIG, False)
            print ("Sensor settling...")
        
            time.sleep(2)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            
            #Obtaining time for the start of the pulse 
            while GPIO.input(ECHO)==0:
              pulseStart = time.time()
            
            # Obtaining time for the end of the pulse
            while GPIO.input(ECHO)==1:
              pulseEnd = time.time()

            pulseDuration = pulseEnd - pulseStart

            distance = pulseDuration * 17150

            distance = round(distance, 2)
            
            #Text to speech engine to give audio feedback
            if distance<=15:
                os.popen( 'espeak "warning, obstacle ahead!" --stdout | aplay 2>/dev/null' )
            print ("Distance:",distance,"cm")

    except KeyboardInterrupt:
        print("Cleaning up!")
        gpio.cleanup()


