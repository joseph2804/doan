from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
for i in range(30):
    sleep(5)
    camera.capture('/home/pi/Desktop/cloudinary-1.22.0/images/image%s.jpg' % i)
camera.stop_preview()