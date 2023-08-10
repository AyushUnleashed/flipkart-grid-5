import csv
from collections import Counter

def get_most_frequent_entries_per_column(csv_file_path, excluded_columns=None):
    most_frequent_entries = {}
    
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            for column_name, value in row.items():
                if column_name not in most_frequent_entries:
                    most_frequent_entries[column_name] = Counter()
                
                if value:
                    most_frequent_entries[column_name][value] += 1
    
    result = {}
    for column_name, entry_counter in most_frequent_entries.items():
        if column_name not in excluded_columns:
            most_common = entry_counter.most_common()
            if most_common:
                max_count = most_common[0][1]
                most_frequent = [entry for entry, count in most_common if count == max_count]
                result[column_name] = most_frequent
            else:
                result[column_name] = []
    
    return result

if __name__ == "__main__":
    input_csv_file = "./userData/user_data_5.csv"  # Replace with your input CSV file name
    excluded_columns = ["productDisplayName", "id"]  # Replace with columns to exclude
    
    most_frequent_entries = get_most_frequent_entries_per_column(input_csv_file, excluded_columns)
    
    for column_name, frequent_entries in most_frequent_entries.items():
        if frequent_entries:
            print(f"{column_name} : {', '.join(frequent_entries)}")
        else:
            print(f"Column '{column_name}' has no frequent entries.")
