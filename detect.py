import requests, json
import cloudinary
import cloudinary.uploader
from picamera import PiCamera
from time import sleep
import os
camera = PiCamera()
camera.start_preview()

cloudinary.config(cloud_name='dcyfnbxuu',
                  api_key='718646468651413',
                  api_secret='kmmxq--u1nRP_djslISleCg7Buk')

urlDetect = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
key = '2b0c4db24bde46acbde80a702092cf53'
headers = {'Ocp-Apim-Subscription-Key': key,
       'content-type':'application/json'
}
if os.path.exists("/home/pi/Desktop/cloudinary-1.22.0/images-detect/image.jpg"):
  os.remove("/home/pi/Desktop/cloudinary-1.22.0/images-detect/image.jpg")
camera.capture('/home/pi/Desktop/cloudinary-1.22.0/images-detect/image.jpg')
sleep(5)
camera.stop_preview()
if os.path.exists("urlDetect.txt"):
  os.remove("urlDetect.txt")
f1 = open("urlDetect.txt", "a")
f = open('images-detect/image.jpg', 'rb')       
result = cloudinary.uploader.upload(f)
f1.write(result['url'] + '\n')
f1.close()
f.close()
f2 = open("urlDetect.txt", "r")
urlTemp = f2.read()
f2.close()
bodyDetect = { 
    "url": urlTemp
}
if os.path.exists("detect.txt"):
  os.remove("detect.txt")
resultDetect = requests.post(urlDetect, headers = headers, data = json.dumps(bodyDetect))
if(resultDetect.status_code == 200):
    print(resultDetect.json())
    with open('detect.txt', 'w') as outfile:
               json.dump(resultDetect.json(), outfile)