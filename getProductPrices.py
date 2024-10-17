import requests
import json

# Get client_id
client_id = json.load(open('digikey_token.json'))['client_id']
# Get the access token
access_token = json.load(open('access_token.json'))['access_token']

# The URL for the API
# url = "api.digikey.com/products/v4/search/{productNumber}/productdetails"
#url = 'https://api.digikey.com/products/v4/search/CL21A106KAYNNNE/productdetails'
#url = 'https://api.digikey.com/products/v4/search/{productNumber}/digireelpricing'
url = 'https://api.digikey.com/products/v4/search/CL21A106KAYNNNE/digireelpricing'

# The headers for the GET request
headers = {
    'X-DIGIKEY-Client-Id': client_id,
    'Authorization': f'Bearer {access_token}',
    'X-DIGIKEY-Locale-Site': 'UK',
    'X-DIGIKEY-Locale-Language': 'en',
    'X-DIGIKEY-Locale-Currency': 'GBP',
    'X-DIGIKEY-Customer-Id': '0'
}

# Query parameters
params = {
    'requestedQuantity': '100'
}

# Make the GET request
response = requests.get(url, headers=headers, params=params)

# Check the response status code
if response.status_code == 200:
    # Print the response
    print(response.json())
else:
    # Print the error message
    print(f"Error: {response.status_code}, {response.text}")