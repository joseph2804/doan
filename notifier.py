import requests, json

url = 'http://notifiermobile.com/api/notifications?username=joseph2804&secretkey=waxsF5roKBxR'
body = {
    "Title": "Auto-Door",
    "Message": "Opened",
    "Type": 1
}
headers = {
	   'content-type':'application/json'
}
res = requests.post(url ,headers = headers, data = json.dumps(body))
print(res.status_code)