import requests

url = "http://localhost:6969/ask"
data = {
    "proxy": "http://qspsowgs:bivxb6sli2f5@142.111.48.253:7030",
    "message": "who is elon musk"
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.json())
