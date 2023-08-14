import pandas as pd

def get_user_purchase_insight(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    most_frequent = []
    columns = ["subCategory", "subCategory", "masterCategory", "masterCategory"]
    subcategory_values = ["topwear", "bottomwear", "footwear", "accessories"]
    
    for i in range(0, 4):
        # Filter data based on the specified subCategory value
        filtered_data = df[df[columns[i]] == subcategory_values[i]]

        if not filtered_data.empty:
            curr_most_frequent = {}
            curr_most_frequent["category"] = subcategory_values[i]
            
            if 'brandName' in filtered_data:
                curr_most_frequent["brandName"] = filtered_data['brandName'].value_counts().idxmax()
            if 'baseColour' in filtered_data:
                curr_most_frequent["baseColour"] = filtered_data['baseColour'].value_counts().idxmax()
            if 'articleType' in filtered_data:
                curr_most_frequent["articleType"] = filtered_data['articleType'].value_counts().idxmax()
            if 'Occasion' in filtered_data:
                curr_most_frequent["Occasion"] = filtered_data['Occasion'].value_counts().idxmax()
            
            most_frequent.append(curr_most_frequent)

    return most_frequent

# Replace these values with your specific file name and subCategory value



if __name__ == "__main__":
    csv_file = "./dataset/user_history_data/gwen.csv"
    most_frequent = get_user_purchase_insight(csv_file)
    for frequent in most_frequent:
        print(frequent)