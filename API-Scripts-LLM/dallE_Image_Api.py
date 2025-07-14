import requests
import json
import pprint
import constants



# API CREDENTIALS
api_secret_key = constants.APIKEY
organization_id = constants.ORGANIZATION_ID







# PASS THIS HEADER TO AUTH EVERY REQUEST
authorized_headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {api_secret_key}",
    'OpenAI-Organization' : organization_id
}



# REQUEST TO API
url = "https://api.openai.com/v1/images/generations"
amount_of_generations = 1
image_request_data = {
    "prompt": "",
    "n": amount_of_generations,
    "size": "256x256"
}
image_request_data["prompt"] = input("Please enter prompt to ask Dall - E: ")
response = requests.post(url, headers=authorized_headers, json=image_request_data)

# DISPLAY OUTPUT
if "data" in  response.json():
    for x in range(0,len(response.json()['data']), 1):
        print() 
        print(response.json()["data"][x]['url'])
        print("\n-------------------------------\n")

else:
    pprint.pprint(response.json())


