import requests, json, cloudinary
import cloudinary.uploader
import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import os
camera = PiCamera()
camera.start_preview()
lockPin = 33
ledPin = 12
pressPin = 22
pressPin1 = 37
ringPin = 16                    # pin11

GPIO.setmode(GPIO.BOARD)            # Numbers GPIOs by physical location
GPIO.setup(ledPin, GPIO.OUT)        # Set LedPin's mode is output
GPIO.setup(lockPin, GPIO.OUT)
GPIO.output(lockPin, GPIO.LOW)
GPIO.output(ledPin, GPIO.LOW)      # Set LedPin high(+3.3V) to turn on led
GPIO.setup(pressPin, GPIO.IN)
GPIO.setup(pressPin1, GPIO.IN)
GPIO.setup(ringPin, GPIO.OUT)
GPIO.output(ringPin, GPIO.LOW)

def capture():
    camera.start_preview()
    for i in range(30):
        if os.path.exists('/home/pi/Desktop/cloudinary-1.22.0/images/image%s.jpg' % i):
            os.remove('/home/pi/Desktop/cloudinary-1.22.0/images/image%s.jpg' % i)
        camera.capture('/home/pi/Desktop/cloudinary-1.22.0/images/image%s.jpg' % i)
        time.sleep(5)
    camera.stop_preview()
    print('capture done!')

def up():
    cloudinary.config(cloud_name='dcyfnbxuu',
                  api_key='718646468651413',
                  api_secret='kmmxq--u1nRP_djslISleCg7Buk')
    if os.path.exists("url.txt"):
        os.remove("url.txt")
    f1 = open("url.txt", "a")
    for i in range(30):  
        f = open('images/image%s.jpg'  % i, 'rb')       
        result = cloudinary.uploader.upload(f)
        f1.write(result['url'] + '\n')
        time.sleep(5)
    f1.close()
    
def createPerson():
    url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/house-owner/persons'
    key = '2b0c4db24bde46acbde80a702092cf53'
    headers = {'Ocp-Apim-Subscription-Key': key,
               'content-type':'application/json'
    }
    bodyPerson = { 
            "name": "Pham Hai Duong",
            "userData": "Admin"
    }
    response = requests.post(url,headers = headers,data = json.dumps(bodyPerson))
    if(response.status_code == 200):
        print('Created Person')
        personId = response.json().get('personId')
        print(personId)
        urlAddFace = url + '/' + personId + '/persistedFaces'
        f = open('url.txt', 'r')
        for x in f:
            data = {
                   'url': x
            }
            res = requests.post(urlAddFace, headers = headers, data = json.dumps(data))
            if(res.status_code == 200):
                print(res.json())
            else:
                print(res.json())
            time.sleep(4)
        f.close()
        urlTrain = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/house-owner/train'
        result = requests.post(urlTrain, headers = headers)
        if (result.status_code == 202):
            print('train done')
        else:
            print(result.json())
        getResult = requests.get(url , headers = headers)
        if(getResult.status_code == 200):
            with open('personList.txt', 'w') as outfile:
               json.dump(getResult.json(), outfile)
        else:
            print(getResult.json())
        with open('personList.txt') as json_file:
            data = json.load(json_file)
            for p in data:
                print('personId: ' + p['personId'])
                
def detect():
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
    time.sleep(5)
    GPIO.output(ringPin, GPIO.HIGH) #ring...
    time.sleep(0.3)
    GPIO.output(ringPin, GPIO.LOW)
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

def cognitive():
    urlCognitive = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/identify'
    key = '2b0c4db24bde46acbde80a702092cf53'
    headers = {'Ocp-Apim-Subscription-Key': key,
               'content-type':'application/json'
              }
    faceIds = []
    bodyCognitive = {}
    with open('detect.txt') as json_file:
        data = json.load(json_file)
        for p in data:
            faceIds.insert(1,p['faceId'])
            bodyCognitive = {
                "personGroupId": "house-owner",
                "faceIds": faceIds,
                "maxNumOfCandidatesReturned": 1,
                "confidenceThreshold": 0.8    
            }
    print(faceIds)
    openDoor = 'false'
    resultCognitive = requests.post(urlCognitive, headers = headers, data = json.dumps(bodyCognitive))
    if(resultCognitive.status_code == 200):
        candidate =  resultCognitive.json()[0].get('candidates')
        personId = ''
        try: 
            personId = candidate[0].get('personId')
        except:
            print('Khong nhan dien duoc chu nha')
        with open('personList.txt') as json_file:
            data = json.load(json_file)
            for p in data:
                if(p['personId'] == personId):
                    openDoor = 'true'
                    print(p)
                    break
    print(openDoor)
    f2 = open("door.txt", "w")
    f2.write(openDoor)
    f2.close()
    
def notifier(mess):
    url = 'http://notifiermobile.com/api/notifications?username=joseph2804&secretkey=waxsF5roKBxR'
    body = {
        "Title": "Auto-Door",
        "Message": mess,
        "Type": 1
    }
    headers = {
           'content-type':'application/json'
    }
    res = requests.post(url ,headers = headers, data = json.dumps(body))
    print(res.status_code)

count = 0
f2 = open("lock.txt", "w")
f2.write('true')
f2.close()
try:
  while True:
    if(GPIO.input(pressPin1) == 1):
        if os.path.exists("lock.txt"):
                f2 = open("lock.txt", "r")
                locked = f2.read()
                f2.close()
        else:
                locked = 'false'
        if(locked == 'false'):
            print('configing...')
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            print('on')
            time.sleep(0.3)
            GPIO.output(ringPin, GPIO.LOW)
            GPIO.output(ledPin, GPIO.LOW)
            capture()
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            time.sleep(0.3)
            GPIO.output(ringPin, GPIO.LOW)
            GPIO.output(ledPin, GPIO.LOW)
            up()
            createPerson()
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            time.sleep(0.3)
            GPIO.output(ringPin, GPIO.LOW)
            GPIO.output(ledPin, GPIO.LOW)
            print('done!')
    if(GPIO.input(pressPin) == 1):
        count = count + 1
        if(count%2 != 0):
            GPIO.output(ledPin, GPIO.HIGH)  # led on
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            print('on')
            time.sleep(0.3)
            GPIO.output(ringPin, GPIO.LOW)
            GPIO.output(ledPin, GPIO.LOW)
            if os.path.exists("lock.txt"):
                f2 = open("lock.txt", "r")
                locked = f2.read()
                f2.close()
            else:
                locked = 'true'
            if(locked == 'true'):
                detect()
                cognitive()
            if os.path.exists("door.txt"):
                f2 = open("door.txt", "r")
                openDoor = f2.read()
                f2.close()
            else:
                openDoor = 'false'
            
            if(openDoor == 'true'):
                locked = 'false'
                GPIO.output(lockPin, GPIO.HIGH)
                notifier('opened')
                f2 = open("lock.txt", "w")
                f2.write(locked)
                f2.close()

        else:
            GPIO.output(ledPin, GPIO.HIGH)
            GPIO.output(ringPin, GPIO.HIGH) #ring...
            print('off')
            time.sleep(0.3)
            GPIO.output(ledPin, GPIO.LOW)   # led off
            GPIO.output(ringPin, GPIO.LOW)
            locked = ''
            if os.path.exists("lock.txt"):
                f2 = open("lock.txt", "r")
                locked = f2.read()
                f2.close()
            else:
                locked = 'true'
            if(locked == 'false'):
                GPIO.output(lockPin, GPIO.LOW)
                notifier('closed')
                locked = 'true'
                f2 = open("lock.txt", "w")
                f2.write(locked)
                f2.close()
            time.sleep(1)
        time.sleep(5)    
except KeyboardInterrupt:           # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
  pass
  GPIO.output(ledPin, GPIO.LOW)     # led off
  GPIO.cleanup()                    # Release resource
