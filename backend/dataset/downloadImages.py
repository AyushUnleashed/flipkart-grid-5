# This files downloads images from the links given  and save them to the ID provided in the CSV file. 





import os
import pandas as pd
import requests
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Create a folder to store downloaded images
output_folder = 'downloaded_images'
os.makedirs(output_folder, exist_ok=True)

# Read the CSV file and detect encoding
csv_file_path = 'choli.csv'  # Replace with the actual path to your CSV file
csv_encoding = detect_encoding(csv_file_path)
data = pd.read_csv(csv_file_path, encoding=csv_encoding)

# Ensure the 'style_image' column exists in the CSV
if 'style_image' not in data.columns:
    print("The 'style_image' column does not exist in the CSV.")
else:
    # Download and save images
    for index, row in data.iterrows():
        image_url = row['style_image']
        image_name = f"{row['id']}.jpg"  # You can modify the naming scheme if needed
        image_path = os.path.join(output_folder, image_name)

        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            with open(image_path, 'wb') as image_file:
                image_file.write(response.content)
            print(f"Downloaded: {image_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {image_name}: {e}")

print("Image download complete.")


    