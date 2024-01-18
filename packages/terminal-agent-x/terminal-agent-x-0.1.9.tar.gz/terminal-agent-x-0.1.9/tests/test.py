import requests
import json

url = "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText?key=AIzaSyDS2_Aa86Jfq1m7moqv2ObQIuT9dlD67zM"

headers = {
    "Content-Type": "application/json"
}

data = {
    "prompt": {
        "text": "Write a story about a magic backpack"
    }
}

json_data = json.dumps(data)

response = requests.post(url, headers=headers, data=json_data)
result = response.json()
print(result)