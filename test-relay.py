import RPi.GPIO as GPIO
import time
LockPin = 3                        # pin11

GPIO.setmode(GPIO.BOARD)            # Numbers GPIOs by physical location
GPIO.setup(LockPin, GPIO.OUT)        # Set LedPin's mode is output
GPIO.output(LockPin, GPIO.HIGH)      # Set LedPin high(+3.3V) to turn on led

try:
  while True:
    GPIO.output(LockPin, GPIO.HIGH)  # led on
    print('on')
    time.sleep(1)
    GPIO.output(LockPin, GPIO.LOW)   # led off
    print('off')
    time.sleep(1)
except KeyboardInterrupt:           # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
  pass
  GPIO.output(LockPin, GPIO.LOW)     # led off
  GPIO.cleanup()                    # Release resource
