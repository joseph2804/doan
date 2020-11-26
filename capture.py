from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
for i in range(30):
    camera.capture('/home/pi/Desktop/cloudinary-1.22.0/images/image%s.jpg' % i)
    sleep(5)
camera.stop_preview()