import requests, json

url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/house-owner/persons'
headers = {'Ocp-Apim-Subscription-Key': key,
       'content-type':'application/json'
}
bodyPerson = { 
    "name": "Pham Hai Duong",
    "userData": "Admin"
}
response = requests.post(urlCreatePerson,headers = headers,data = json.dumps(bodyPerson))
if(response.status_code == 200):
    print('Created Person')
    personId = response.json().get('personId')
    urlAddFace = url + '/' + personId + '/persistedFaces'
    f = open('url.txt', 'r')
    for x in f:
       data = {
           "url": x
       }
       res = requests.post(url, headers = headers, data = json.dumps(data))
       if(res.status_code == 200):
           print(res.json())
       else:
           print(res.status_code)
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
    urlDetect = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    bodyDetect = {
        "url": "http://example.com/1.jpg"
    }
    resultDetect = requests.post(url , headers = headers)
    if(resultDetect.status_code == 200):
        for temp in resultDetect.json().get('faceId'):
            print(temp)
    
    