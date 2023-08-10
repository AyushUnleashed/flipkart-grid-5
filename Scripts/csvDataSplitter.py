import csv
import os

def split_csv(input_file, output_directory, chunk_size, num_output_files):
    with open(input_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Assuming the first row is the header
        
        entries = []
        file_counter = 1
        
        for row in reader:
            entries.append(row)
            
            if len(entries) == chunk_size:
                output_file = os.path.join(output_directory, f'user_data_{file_counter}.csv')
                with open(output_file, 'w', newline='') as output_csv:
                    writer = csv.writer(output_csv)
                    writer.writerow(header)
                    writer.writerows(entries)
                
                entries = []
                file_counter += 1
                
                if file_counter > num_output_files:
                    break
        
        if entries and file_counter <= num_output_files:
            output_file = os.path.join(output_directory, f'user_data_{file_counter}.csv')
            with open(output_file, 'w', newline='') as output_csv:
                writer = csv.writer(output_csv)
                writer.writerow(header)
                writer.writerows(entries)

if __name__ == "__main__":
    input_csv_file = "./data/styles.csv"  # Replace with your input CSV file name
    output_folder = "./userData/"  # Replace with the desired output directory
    # number of entries in one output file
    chunk_size = 50
    # number of output files
    num_output_files = 5
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    split_csv(input_csv_file, output_folder, chunk_size, num_output_files)
    print("CSV splitting complete.")
