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
    extracted_data["product_display_name"] = data_info.get("productDisplayName", "none").lower()
    extracted_data["brand_name"] = data_info.get("brandName", "none").lower()
    master_category = data_info.get("masterCategory", {})
    extracted_data["master_category"] = master_category.get("typeName", "none").lower()
    
    sub_category = data_info.get("subCategory", {})
    extracted_data["sub_category"] = sub_category.get("typeName", "none").lower()
    extracted_data["article_type"] = data_info.get("articleType", {}).get("typeName", "none").lower()
    extracted_data["age_group"] = data_info.get("ageGroup", "none").lower()
    extracted_data["gender"] = data_info.get("gender", "none").lower()
    extracted_data["color"] = data_info.get("baseColour", "none").lower()
    extracted_data["season"] = data_info.get("season", "none").lower()
    extracted_data["usage"] = data_info.get("usage", "none").lower()
    
    article_attributes = data_info.get("articleAttributes", {})
    extracted_data["fit"] = article_attributes.get("Fit", "none").lower()
    extracted_data["pattern"] = article_attributes.get("Pattern", "none").lower()
    extracted_data["shape"] = article_attributes.get("Shape", "none").lower()
    extracted_data["occasion"] = article_attributes.get("Occasion", "none").lower()
    extracted_data["sleeve_styling"] = article_attributes.get("Sleeve Styling", "none").lower()
    extracted_data["sleeve_length"] = article_attributes.get("Sleeve Length", "none").lower()
    extracted_data["fabric"] = article_attributes.get("Fabric", "none").lower()
    extracted_data["neck"] = article_attributes.get("Neck", "none").lower()
    other_flags_list = data_info.get("otherFlags", [])
    other_flags = extract_other_flags(other_flags_list)
    if len(other_flags) != 0:
        extracted_data["is_jewellery"] = other_flags[0].get("value", "none").lower()
    else:
        extracted_data["is_jewellery"] = "none"
    
    product_descriptors = data_info.get("productDescriptors", {})
    description_value = product_descriptors.get("description", {}).get("value", "none").lower()
    extracted_data["product_description1"] = extract_text_from_html(description_value).lower()
    
    style_images = data_info.get("styleImages", {}).get("default", {})
    extracted_data["style_image"] = style_images.get("imageURL", "none")
    extracted_data["landing_page_url"] = data_info.get("landingPageUrl", "none")
    
    return extracted_data

# Iterate through JSON files and extract data
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8-sig") as file:
            try:
                json_data = json.load(file)
                extracted_data = extract_keys(json_data)
                if extracted_data["age_group"] in ["kids-girls", "kids-boys", "kids-unisex"]:
                    continue
                output_data.append(extracted_data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(output_data)

# Define the column order for the CSV file
column_order = ["id", "product_display_name", "brand_name", "master_category", "sub_category", "article_type", "gender", "color", "season", "usage", "fit", "pattern", "shape", "occasion", "sleeve_styling", "sleeve_length", "fabric", "neck", "is_jewellery", "product_description1", "style_image", "landing_page_url"]

# Append the DataFrame to a CSV file
csv_filename = "./new_data_set/new_data_set.csv"
df[column_order].to_csv(csv_filename, index=False)

print(f"Data has been appended to {csv_filename}")
