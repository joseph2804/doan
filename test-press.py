import RPi.GPIO as GPIO
import time, os
lockPin = 33
ledPin = 12
pressPin = 22 
ringPin = 16                    # pin11

GPIO.setmode(GPIO.BOARD)            # Numbers GPIOs by physical location
GPIO.setup(ledPin, GPIO.OUT)        # Set LedPin's mode is output
GPIO.setup(lockPin, GPIO.OUT)
GPIO.output(lockPin, GPIO.HIGH)
GPIO.output(ledPin, GPIO.LOW)      # Set LedPin high(+3.3V) to turn on led
GPIO.setup(pressPin, GPIO.IN)
GPIO.setup(ringPin, GPIO.OUT)
GPIO.output(ringPin, GPIO.LOW)
count = 0
try:
  while True:
    if(GPIO.input(pressPin) == 1):
        count = count + 1
        if(count%2 != 0):
            if os.path.exists("lock.txt"):
                f2 = open("lock.txt", "r")
                locked = f2.read()
                f2.close()
            else:
                locked = 'false'
            
            if(locked == 'false'):
                locked = 'true'
                GPIO.output(lockPin, GPIO.LOW)
                f2 = open("lock.txt", "w")
                f2.write(locked)
                f2.close()
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            print('on')
            time.sleep(0.2)
            GPIO.output(ringPin, GPIO.LOW)
            GPIO.output(ledPin, GPIO.LOW)

        else:
            locked = 'false'
            GPIO.output(lockPin, GPIO.LOW)
            f2 = open("lock.txt", "w")
            f2.write(locked)
            f2.close()
            GPIO.output(ledPin, GPIO.HIGH)
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            print('off')
            time.sleep(0.2)
            GPIO.output(ledPin, GPIO.LOW)   # led off
            GPIO.output(ringPin, GPIO.LOW)
except KeyboardInterrupt:           # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
  pass
  GPIO.output(ledPin, GPIO.LOW)     # led off
  GPIO.cleanup()                    # Release resource
