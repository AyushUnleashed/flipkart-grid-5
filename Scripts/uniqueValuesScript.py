import pandas as pd
import json
import numpy as np

def save_unique_values_to_json(file_path, excluded_columns, json_output_file):
    # Read CSV file using pandas, excluding specified columns
    df = pd.read_csv(file_path, usecols=lambda column: column not in excluded_columns)
    
    # Replace "none" and NaN values with np.nan
    df.replace(['none', np.nan], np.nan, inplace=True)
    
    # Dictionary to store column-wise unique values
    column_unique_values = {}
    
    # Loop through each column in the DataFrame
    for column in df.columns:
        unique_values = df[column].dropna().unique()  # Drop NaN values
        # Convert ndarray to list and store as a value in the dictionary
        column_unique_values[column] = unique_values.tolist()
        
    # Write the unique values dictionary to the JSON file
    with open(json_output_file, 'w') as json_file:
        json.dump(column_unique_values, json_file, indent=4)

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'Scripts/new_data_set/new_data_set_modified.csv'
excluded_columns = ['id', 'productDisplayName', 'masterCategory', 'subCategory', 'landingPageUrl', 'styleImage', 'gender', 'isJewellery', 'productDescription1']  # Add columns to exclude
json_output_file = 'Scripts/unique_values/unique_values.json'  # Output JSON file path

save_unique_values_to_json(file_path, excluded_columns, json_output_file)
