import tkinter as tk
from tkinter import filedialog
import os

# Function to open the file explorer
def open_file():
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
start_pricing_button = tk.Button(root, text="Start Pricing", command=lambda: print("Pricing started"))
start_pricing_button.pack(pady=10)

# Start the main event loop
root.mainloop()