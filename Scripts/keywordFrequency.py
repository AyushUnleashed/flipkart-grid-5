import csv
from collections import defaultdict
from openpyxl import Workbook

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = './data/myntradataset/styles.csv'
# Replace 'column_name' with the name of the column containing keywords
column_name = 'gender'

# Open the CSV file in read mode
with open(csv_file_path, 'r') as csv_file:
    # Create a CSV reader object
    csv_reader = csv.DictReader(csv_file)
    
    # Initialize a defaultdict to store the keyword frequencies
    keyword_frequencies = defaultdict(int)
    
    # Loop through each row in the CSV file
    for row in csv_reader:
        keyword_text = row[column_name]
        keywords = keyword_text.split()  # Split keywords using space as delimiter
        
        for keyword in keywords:
            keyword_frequencies[keyword] += 1

# Create a new Excel workbook
workbook = Workbook()
sheet = workbook.active

# Write header row
sheet.append(['Keyword', 'Frequency'])

# Write keyword frequency data
for keyword, frequency in keyword_frequencies.items():
    sheet.append([keyword, frequency])

# Save the Excel file
excel_file_path = 'gender.xlsx'
workbook.save(excel_file_path)
print(f"Keyword frequency data saved to '{excel_file_path}'.")
