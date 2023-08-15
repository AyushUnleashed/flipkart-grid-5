import pandas as pd

def get_user_purchase_insight(csv_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file, encoding='ISO-8859-1')

    most_frequent = []
    columns = ["sub_category", "sub_category", "master_category", "master_category"]
    subcategory_values = ["topwear", "bottomwear", "footwear", "accessories"]
    
    for i in range(0, 4):
        # Filter data based on the specified subCategory value
        filtered_data = df[df[columns[i]] == subcategory_values[i]]

        if not filtered_data.empty:
            curr_most_frequent = {}
            curr_most_frequent["category"] = subcategory_values[i]
            
            if 'brand_name' in filtered_data:
                curr_most_frequent["brand_name"] = filtered_data['brand_name'].value_counts().idxmax()
            if 'color' in filtered_data:
                curr_most_frequent["color"] = filtered_data['color'].value_counts().idxmax()
            if 'article_type' in filtered_data:
                curr_most_frequent["article_type"] = filtered_data['article_type'].value_counts().idxmax()
            if 'occasion' in filtered_data:
                curr_most_frequent["occasion"] = filtered_data['occasion'].value_counts().idxmax()
            
            most_frequent.append(curr_most_frequent)

    return most_frequent

# Replace these values with your specific file name and subCategory value



if __name__ == "__main__":
    csv_file = "./dataset/user_history_data/gwen.csv"
    most_frequent = get_user_purchase_insight(csv_file)
    for frequent in most_frequent:
        print(frequent)