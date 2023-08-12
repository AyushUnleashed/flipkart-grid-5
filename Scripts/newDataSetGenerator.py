import os
import json
import pandas as pd

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

def extract_keys(data):
    extracted_data = {}
    
    data_info = data.get("data", {})
    extracted_data["id"] = data_info.get("id", "none")
    extracted_data["productDisplayName"] = data_info.get("productDisplayName", "none")
    extracted_data["variantName"] = data_info.get("variantName", "none")
    extracted_data["brandName"] = data_info.get("brandName", "none")
    extracted_data["ageGroup"] = data_info.get("ageGroup", "none")
    extracted_data["gender"] = data_info.get("gender", "none")
    extracted_data["baseColour"] = data_info.get("baseColour", "none")
    extracted_data["fashionType"] = data_info.get("fashionType", "none")
    extracted_data["season"] = data_info.get("season", "none")
    extracted_data["usage"] = data_info.get("usage", "none")
    extracted_data["displayCategories"] = data_info.get("displayCategories", "none")
    extracted_data["landingPageUrl"] = data_info.get("landingPageUrl", "none")
    
    article_attributes = data_info.get("articleAttributes", "none")
    extracted_data["Fit"] = article_attributes.get("Fit", "none")
    extracted_data["Pattern"] = article_attributes.get("Pattern", "none")
    extracted_data["Shape"] = article_attributes.get("Shape", "none")
    extracted_data["Occasion"] = article_attributes.get("Occasion", "none")
    extracted_data["Sleeve styling"] = article_attributes.get("Sleeve styling", "none")
    extracted_data["Sleeve length"] = article_attributes.get("Sleeve length", "none")
    extracted_data["Fabric"] = article_attributes.get("Fabric", "none")
    extracted_data["Neck"] = article_attributes.get("Neck", "none")
    
    style_images = data_info.get("styleImages", {}).get("default", {})
    extracted_data["styleImage"] = style_images.get("imageURL", "none")
    
    master_category = data_info.get("masterCategory", {})
    extracted_data["masterCategory"] = master_category.get("typeName", "none")
    
    sub_category = data_info.get("subCategory", {})
    extracted_data["subCategory"] = sub_category.get("typeName", "none")
    
    other_flags_list = data_info.get("otherFlags", [])
    other_flags = extract_other_flags(other_flags_list)
    if len(other_flags) != 0:
        extracted_data["isJewellery"] = other_flags[0].get("value", "none")
    else:
        extracted_data["isJewellery"] = "none"
    
    product_descriptors = data_info.get("productDescriptors", {})
    extracted_data["productDescription1"] = product_descriptors.get("description", {}).get("value", "none")
    extracted_data["productDescription2"] = product_descriptors.get("style_note", {}).get("value", "none")
    
    extracted_data["articleType"] = data_info.get("articleType", {}).get("typeName", "none")
    
    return extracted_data

# file_count = 0
for filename in os.listdir(input_folder):
    # if file_count >= 20000:
    #     break
    
    if filename.endswith(".json"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8-sig") as file:
            try:
                json_data = json.load(file)
                extracted_data = extract_keys(json_data)
                if extracted_data["ageGroup"] == "Kids-Girls" or extracted_data["ageGroup"] == "Kids-Boys":
                    continue
                output_data.append(extracted_data)
                # file_count += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file: {filename}")

# Create a pandas DataFrame from the extracted data
df = pd.DataFrame(output_data)

# Define the column order for the CSV file
column_order = ["id", "productDisplayName", "variantName", "brandName", "ageGroup", "gender", "baseColour",
                "fashionType", "season", "usage", "displayCategories", "landingPageUrl", "styleImage",
                "masterCategory", "subCategory", "isJewellery", "productDescription1", "productDescription2",
                "articleType"]

# Append the DataFrame to a CSV file
csv_filename = "./new_data_set/new_data_set.csv"
df[column_order].to_csv(csv_filename, index=False)

print(f"Data has been appended to {csv_filename}")
