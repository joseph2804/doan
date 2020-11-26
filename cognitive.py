import requests, json
import array as arr

urlCognitive = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/identify'
key = '2b0c4db24bde46acbde80a702092cf53'
headers = {'Ocp-Apim-Subscription-Key': key,
       'content-type':'application/json'
}
faceIds = []
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
    personId = candidate[0].get('personId')
    with open('personList.txt') as json_file:
        data = json.load(json_file)
        for p in data:
                if(p['personId'] == personId):
                    openDoor = 'true'
                    print(p)
                    break
print(openDoor)

