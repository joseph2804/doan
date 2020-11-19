import cloudinary
import cloudinary.uploader
import json
from time import sleep

cloudinary.config(cloud_name='dcyfnbxuu',
                  api_key='718646468651413',
                  api_secret='kmmxq--u1nRP_djslISleCg7Buk')
f1 = open("url.txt", "a")
for i in range(30):  
    f = open('images/image%s.jpg'  % i, 'rb')       
    result = cloudinary.uploader.upload(f)
    f1.write(result['url'] + '\n')
    sleep(5)
f1.close()