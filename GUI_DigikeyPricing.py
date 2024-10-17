import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import json
import requests
import pandas as pd
import csv

# Global variable to store the selected file path
selected_file_path = None

# Function to open the file explorer
def open_file():
    global selected_file_path
    # Open the file explorer
    file_path = filedialog.askopenfilename(
        title="Select CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        # Get the name of the selected file from the path
        file_name = os.path.basename(file_path)
        # Update the label with the selected file name
        selected_file_label.config(text=f"Selected File: {file_name}")
        # Save the file path of the selected file
        selected_file_path = file_path


def get_prices():
    global selected_file_path
    # Ensure file is selected
    if not selected_file_path:
        messagebox.showerror("Error", "Please select a CSV file")
        return
    
    # Ensure number of sets is entered
    if not number_of_sets_entry.get():
        messagebox.showerror("Error", "Please enter the number of sets")
        return

    # Run the getAccessToken.py script to get a new access token
    print('Getting a new access token...')
    subprocess.run(['python', 'getAccessToken.py'])

    # Get client_id
    client_id = json.load(open('digikey_token.json'))['client_id']
    # Get the access token
    access_token = json.load(open('access_token.json'))['access_token']

    # Open the CSV file
    csv_filename = selected_file_path
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

    # Error CSV file name
    error_csv_filename = 'price_details_ERRORS.csv'

    # Open the csv file in write mode
    with open(output_csv_filename, mode='w', newline='') as f:
        csv_writer = csv.writer(f)

        # Write the header to the CSV file
        csv_writer.writerow(csv_header)

        # Initialize a list to store the rows with errors
        error_rows = []

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
            set_quantity = quantity * int(number_of_sets_entry.get())

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
                # Add the row to the list of error rows
                error_rows.append([stock_code, set_quantity, quantity, 'N/A', 'N/A', 'N/A', response.text])

        # Save the rows with errors to a separate CSV file
    if error_rows:
        with open(error_csv_filename, mode='w', newline='') as error_file:
            error_writer = csv.writer(error_file)
            error_writer.writerow(csv_header)  # Write the header
            error_writer.writerows(error_rows)  # Write the error rows

    df = pd.read_csv(output_csv_filename)
    # Ignore any rows with 'N/A' in the 'ExtendedPrice' column
    total_extended_price = df[df['ExtendedPrice'] != 'N/A']['ExtendedPrice'].sum()
    # Round the total extended price to 2 decimal places
    total_extended_price = round(total_extended_price, 2)
    print('Total Extended Price:', total_extended_price)
    # Print a message indicating the process is complete
    print('Price details saved to', output_csv_filename)
    # Get the output file path
    output_file_path = os.path.abspath(output_csv_filename)

    # Check for any errors in the CSV
    error_rows = df[df['Error'] != 'N/A']
    if not error_rows.empty:
        # Add a label to notify the user that there were errors
        error_label = tk.Label(root, text="Warning: There were errors in getting prices.", fg="red")
        error_label.pack(pady=10)
        # Add a button to display the error file
        error_button = tk.Button(root, text="View Errors File", command=lambda: display_csv_contents(error_csv_filename))
        error_button.pack(pady=10)
        # Add a label to display name of the error file
        error_file_label = tk.Label(root, text=f"Error details saved to {error_csv_filename}", fg="red")
        error_file_label.pack(pady=10)


    # Add a label to display the total extended price
    total_price_label = tk.Label(root, text=f"Total Extended Price: {total_extended_price}")
    total_price_label.pack(pady=10)

    # Add a label to display the output file name
    output_file_label = tk.Label(root, text=f"Price details saved to {output_csv_filename}")
    output_file_label.pack(pady=10)

    # Add a button to open the output file in the default application
    open_output_file_button = tk.Button(root, text="Open Output File", command=lambda: display_csv_contents(output_file_path))
    open_output_file_button.pack(pady=10)

    

def display_csv_contents(file_path):
    try:
        # Read the CSV file using pandas
        df = pd.read_csv(file_path)
        
        # Create a new window to display the CSV contentsa
        csv_window = tk.Toplevel(root)
        csv_window.title("CSV File Contents")
        csv_window.geometry("600x400")
        
        # Create a Treeview widget to display the data in a table format
        tree = ttk.Treeview(csv_window)
        tree.pack(expand=True, fill='both')

        # Define the columns
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"

        # Create the column headings
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Add the rows from the DataFrame
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")

# Create the main window
root = tk.Tk()
root.title("Digikey Pricing")
root.geometry("600x400")

# Create a label to display the selected file name
selected_file_label = tk.Label(root, text="No file selected")
selected_file_label.pack(pady=20)

# Create a button to open the file explorer
select_csv_button = tk.Button(root, text="Select CSV File", command=open_file)
select_csv_button.pack(pady=10)

# Create a label for the number of sets
number_of_sets_label = tk.Label(root, text="Enter the number of sets:")
number_of_sets_label.pack(pady=10)

# Create an input box for the number of sets
number_of_sets_entry = tk.Entry(root)
number_of_sets_entry.pack(pady=10)

# Create a button to start the pricing process
start_pricing_button = tk.Button(root, text="Start Pricing", command=get_prices)
start_pricing_button.pack(pady=10)

# Start the main event loop
root.mainloop()