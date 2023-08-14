import os
import json
import pandas as pd
from bs4 import BeautifulSoup

input_folder = "./styles/"
output_data = []

keys_to_extract = ["dataType", "name", "value"]

def extract_other_flags(other_flags_list):
    extracted_flags = []
    for flag in other_flags_list:
        if flag.get("name") == "isJewellery":
            extracted_flag = {}
            for key in keys_to_extract:
                extracted_flag[key] = flag.get(key, "none")
            extracted_flags.append(extracted_flag)
            break
    return extracted_flags

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def extract_keys(data):
    extracted_data = {}
    
    data_info = data.get("data", {})
    extracted_data["id"] = data_info.get("id", "none")
    extracted_data["productDisplayName"] = data_info.get("productDisplayName", "none").lower()
    extracted_data["brandName"] = data_info.get("brandName", "none").lower()
    master_category = data_info.get("masterCategory", {})
    extracted_data["masterCategory"] = master_category.get("typeName", "none").lower()
    
    sub_category = data_info.get("subCategory", {})
    extracted_data["subCategory"] = sub_category.get("typeName", "none").lower()
    extracted_data["articleType"] = data_info.get("articleType", {}).get("typeName", "none").lower()
    extracted_data["ageGroup"] = data_info.get("ageGroup", "none").lower()
    extracted_data["gender"] = data_info.get("gender", "none").lower()
    extracted_data["baseColour"] = data_info.get("baseColour", "none").lower()
    extracted_data["season"] = data_info.get("season", "none").lower()
    extracted_data["usage"] = data_info.get("usage", "none").lower()
    
    article_attributes = data_info.get("articleAttributes", {})
    extracted_data["Fit"] = article_attributes.get("Fit", "none").lower()
    extracted_data["Pattern"] = article_attributes.get("Pattern", "none").lower()
    extracted_data["Shape"] = article_attributes.get("Shape", "none").lower()
    extracted_data["Occasion"] = article_attributes.get("Occasion", "none").lower()
    extracted_data["Sleeve styling"] = article_attributes.get("Sleeve Styling", "none").lower()
    extracted_data["Sleeve length"] = article_attributes.get("Sleeve Length", "none").lower()
    extracted_data["Fabric"] = article_attributes.get("Fabric", "none").lower()
    extracted_data["Neck"] = article_attributes.get("Neck", "none").lower()
    other_flags_list = data_info.get("otherFlags", [])
    other_flags = extract_other_flags(other_flags_list)
    if len(other_flags) != 0:
        extracted_data["isJewellery"] = other_flags[0].get("value", "none").lower()
    else:
        extracted_data["isJewellery"] = "none"
    
    product_descriptors = data_info.get("productDescriptors", {})
    description_value = product_descriptors.get("description", {}).get("value", "none").lower()
    extracted_data["productDescription1"] = extract_text_from_html(description_value).lower()
    
    style_images = data_info.get("styleImages", {}).get("default", {})
    extracted_data["styleImage"] = style_images.get("imageURL", "none")
    extracted_data["landingPageUrl"] = data_info.get("landingPageUrl", "none")
    
    return extracted_data

# Iterate through JSON files and extract data
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8-sig") as file:
            try:
                json_data = json.load(file)
                extracted_data = extract_keys(json_data)
                if extracted_data["ageGroup"] in ["kids-girls", "kids-boys", "kids-unisex"]:
                    continue
                output_data.append(extracted_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(output_data)

# Define the column order for the CSV file
column_order = ["id", "productDisplayName", "brandName", "masterCategory", "subCategory", "articleType", "gender", "baseColour", "season", "usage", "Fit", "Pattern", "Shape", "Occasion", "Sleeve styling", "Sleeve length", "Fabric", "Neck", "isJewellery", "productDescription1", "styleImage", "landingPageUrl"]

# Append the DataFrame to a CSV file
csv_filename = "./new_data_set/new_data_set.csv"
df[column_order].to_csv(csv_filename, index=False)

print(f"Data has been appended to {csv_filename}")
