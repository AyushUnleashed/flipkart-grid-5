def extract_category_info(data):
    categories = {
        "topwear": {},
        "bottomwear": {},
        "footwear": {},
        "accessories": {}
    }
    categories_array = ["topwear", "bottomwear", "footwear", "accessories"]

    for i, item in enumerate(data["outfit"]):
        category = categories_array[i]  # Get category based on index
        info = {
            "product_display_name": item["product_display_name"],
            "brand_name": item["brand_name"],
            "color": item["color"],
            "article_type": item["article_type"],
            "master_category": item["master_category"]
        }
        categories[category] = info

    return categories