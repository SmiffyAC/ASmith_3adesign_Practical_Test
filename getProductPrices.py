import requests
import json
import pandas as pd
import csv

# Get client_id
client_id = json.load(open('digikey_token.json'))['client_id']
# Get the access token
access_token = json.load(open('access_token.json'))['access_token']

# Ask the client for a number of sets
number_of_sets = input('Enter the number of sets: ')

# Open the CSV file
csv_filename = 'Bill Of Materials PowerPortMax-v5.csv'
df = pd.read_csv(csv_filename)

# Put the stock codes in a list
stock_codes = df['Stock Code'].tolist()
# Put the quantities in a list
quantities_needed = df['Quantity'].tolist()

# Print the lists
print(stock_codes)
print(quantities_needed)

# CSV output file name
output_csv_filename = 'price_details.csv'
# Define the headers for the CSV file
csv_header = ['Stock Code', 'Total Quantity', 'Quantity Per Set', 'ReelingFee', 'UnitPrice', 'ExtendedPrice', 'Error']

# Open the csv file in write mode
with open(output_csv_filename, mode='w', newline='') as f:
    csv_writer = csv.writer(f)

    # Write the header to the CSV file
    csv_writer.writerow(csv_header)

    # Loop through the stock codes and quantities
    for stock_code, quantity in zip(stock_codes, quantities_needed):
        # The URL for the API
        url = f'https://api.digikey.com/products/v4/search/{stock_code}/digireelpricing'

        # The headers for the GET request
        headers = {
            'X-DIGIKEY-Client-Id': client_id,
            'Authorization': f'Bearer {access_token}',
            'X-DIGIKEY-Locale-Site': 'UK',
            'X-DIGIKEY-Locale-Language': 'en',
            'X-DIGIKEY-Locale-Currency': 'GBP',
            'X-DIGIKEY-Customer-Id': '0'
        }

        # Multiply the quantity by the number of sets
        set_quantity = quantity * int(number_of_sets)

        # Query parameters
        params = {
            'requestedQuantity': set_quantity
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check the response status code
        if response.status_code == 200:
            # Print the response
            print(response.json())
            json_response = response.json()
            # Extract data from the API response (defaulting to 'N/A' if not present)
            reeling_fee = json_response.get('ReelingFee', 'N/A')
            unit_price = json_response.get('UnitPrice', 'N/A')
            extended_price = json_response.get('ExtendedPrice', 'N/A')
            # Write the data to the CSV file
            csv_writer.writerow([stock_code, set_quantity, quantity, reeling_fee, unit_price, extended_price, 'N/A'])
        else:
            # Print the error message
            print(f"Error: {response.status_code}, {response.text}")
            # Write the error message to the CSV file
            csv_writer.writerow([stock_code, set_quantity, quantity, 'N/A', 'N/A', 'N/A', response.text])

# Print a message indicating the process is complete
print('Price details saved to', output_csv_filename)