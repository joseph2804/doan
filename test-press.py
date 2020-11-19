import RPi.GPIO as GPIO
import time
LockPin = 12   
pressPin = 22 
ringPin = 16                    # pin11

GPIO.setmode(GPIO.BOARD)            # Numbers GPIOs by physical location
GPIO.setup(LockPin, GPIO.OUT)        # Set LedPin's mode is output
GPIO.output(LockPin, GPIO.LOW)      # Set LedPin high(+3.3V) to turn on led
GPIO.setup(pressPin, GPIO.IN)
GPIO.setup(ringPin, GPIO.OUT)
GPIO.output(ringPin, GPIO.LOW)
count = 0
try:
  while True:
    if(GPIO.input(pressPin) == 1):
	count = count + 1
	if(count%2 != 0):
    		GPIO.output(LockPin, GPIO.HIGH)  # led on
		GPIO.output(ringPin, GPIO.HIGH) #ring...
    		print('on')
		time.sleep(0.3)
		GPIO.output(ringPin, GPIO.LOW)

    	else:
    		GPIO.output(LockPin, GPIO.LOW)   # led off
		GPIO.output(ringPin, GPIO.HIGH) #ring...
    		print('off')
		time.sleep(0.3)
		GPIO.output(ringPin, GPIO.LOW)
except KeyboardInterrupt:           # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
  pass
  GPIO.output(LockPin, GPIO.LOW)     # led off
  GPIO.cleanup()                    # Release resource
