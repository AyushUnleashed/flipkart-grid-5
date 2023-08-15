import csv
from collections import defaultdict

csv_file_path = 'dataset/top_100.csv'
column_name = 'sub_category'
entry_value = 'bottomwear'

with open(csv_file_path, 'r') as csv_file :
    csv_reader = csv.DictReader(csv_file)
    frequency = 0
    for row in  csv_reader :
        if(row[column_name] == entry_value):
            frequency += 1
    print(frequency)