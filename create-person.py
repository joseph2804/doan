import requests, json
import time

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
    