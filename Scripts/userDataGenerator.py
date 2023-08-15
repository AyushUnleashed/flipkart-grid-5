import csv
# import os
import random

def split_filtered_csv(input_file, output_file, num_entries_per_type):
    with open(input_file, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        header = reader.fieldnames
        
        female_tops_entries = []
        female_skirts_entries = []
        female_shoes_entries = []
        
        for row in reader:
            gender = row.get('gender').strip()  # Removing any extra spaces
            article_type = row.get('article_type').strip()  # Removing any extra spaces
            
            if gender == 'women' and article_type == 'tops' and len(female_tops_entries) < num_entries_per_type:
                female_tops_entries.append(row)
            elif gender == 'women' and article_type == 'skirts' and len(female_skirts_entries) < num_entries_per_type:
                female_skirts_entries.append(row)
            elif gender == 'women' and article_type == 'casual_shoes' and len(female_shoes_entries) < num_entries_per_type:
                female_shoes_entries.append(row)
            
            if len(female_tops_entries) >= num_entries_per_type and len(female_skirts_entries) >= num_entries_per_type and len(female_shoes_entries) >= num_entries_per_type:
                break
        
        female_entries = female_tops_entries + female_skirts_entries + female_shoes_entries
        random.shuffle(female_entries)  # Shuffle the combined list
        
        print("Number of female tops entries:", len(female_tops_entries))
        print("Number of female skirts entries:", len(female_skirts_entries))
        print("Number of female shoes entries:", len(female_shoes_entries))
        
        with open(output_file, 'w', newline='') as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=header)
            writer.writeheader()
            writer.writerows(female_entries)

if __name__ == "__main__":
    input_csv_file = "dataset/main_dataset.csv"  # Replace with your input CSV file name
    output_csv_file = "dataset/user_history_data/gwen.csv"  # Replace with the desired output CSV file name
    num_entries_per_type = 15
    
    split_filtered_csv(input_csv_file, output_csv_file, num_entries_per_type)
    print("Filtered CSV creation complete.")
