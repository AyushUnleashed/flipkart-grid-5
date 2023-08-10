import csv
from openpyxl import Workbook

# Replace 'input_file.csv' with the actual path to your CSV file
csv_file_path = './data/myntradataset/styles.csv'
# Replace 'Keyword' with the column header where you want to search for the keyword
column_name = 'articleType'
# Replace 'your_keyword' with the keyword you want to search for
target_keyword = 'Tshirts'

# Create a new Excel workbook
workbook = Workbook()
sheet = workbook.active

# Write header row in the Excel sheet
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)
    sheet.append(headers)

    # Find the index of the target column
    column_index = headers.index(column_name)

    # Loop through each row in the CSV file
    for row in csv_reader:
        # Check if the keyword exists in the target column
        if row[column_index] == target_keyword:
            sheet.append(row)

# Save the Excel file
excel_file_path = 'output_file.xlsx'
workbook.save(excel_file_path)
print(f"Entries with keyword '{target_keyword}' saved to '{excel_file_path}'.")
