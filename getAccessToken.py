import requests
import json

# The token endpoint
url = 'https://api.digikey.com/v1/oauth2/token'

# JSON file containing the client_id and client_secret
token_filename = 'digikey_token.json'

token = json.load(open(token_filename))

# Data to be sent to the token endpoint
data = {
    'client_id': token['client_id'],
    'client_secret': token['client_secret'],
    'grant_type': 'client_credentials'
}

# Make the POST request
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    # Print the access token
    print('ACCESS TOKEN = ' + response.json()['access_token'])
    # Print the expiration time
    print('EXPIRES IN = ' + str(response.json()['expires_in']))
    # Print the token type
    print('TOKEN TYPE = ' + response.json()['token_type'])
    # Store the access token in a file
    with open('access_token.json', 'w') as f:
        json.dump(response.json(), f)
else:
    print('Error:', response.status_code, response.text)