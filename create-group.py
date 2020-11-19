import requests, json, os

urlPersonGroup = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/persongroups/house-owner'
key = '69f691da2de34340b4217689bb962f62'
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
