import csv

def process_entry(entry):
    return entry.replace(" ", "_").replace("-", "_")

def process_csv(input_file, output_file, columns_to_process):
    with open(input_file, 'r', encoding='utf-8-sig') as input_csv, open(output_file, 'w', newline='', encoding='utf-8') as output_csv:
        reader = csv.DictReader(input_csv)
        
        for column in columns_to_process:
            if column not in reader.fieldnames:
                print(f"Column '{column}' not found in the CSV file.")
                return
        
        writer = csv.DictWriter(output_csv, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            for column in columns_to_process:
                row[column] = process_entry(row[column])
            writer.writerow(row)

    print("Processing complete. Output saved to", output_file)

if __name__ == "__main__":
    input_file = "Scripts/new_data_set/new_data_set.csv"
    output_file = "Scripts/new_data_set/new_data_set_modified.csv"
    columns_to_process = ["brandName", "baseColour", "masterCategory", "subCategory", "articleType", "usage", "Fit", "Pattern", "Shape", "Occasion", "Sleeve styling", "Sleeve length", "Fabric", "Neck"]

    process_csv(input_file, output_file, columns_to_process)
