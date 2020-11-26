import requests, json, os

urlPersonGroup = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/house-owner'
key = '2b0c4db24bde46acbde80a702092cf53'
headers = {'Ocp-Apim-Subscription-Key': key,
       'content-type':'application/json'
}
body = { 
    "name": "Group-Owner",
    "userData": "House Owner"
}

response = requests.put(urlPersonGroup,headers = headers,data = json.dumps(body))
if(response.status_code == 200):
    print('ok')
else:
    print('exist')
