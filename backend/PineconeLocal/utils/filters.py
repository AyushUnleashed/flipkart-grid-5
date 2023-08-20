
def build_hard_filters( occasion=None, article_type=None, color=None, brand_name=None,
                       gender=None, is_jewellery=None, master_category=None,
                       product_display_name=None, season=None, style_image=None,
                       sub_category=None):
    hard_filters = {}

    if occasion is not None: hard_filters["occasion"] = {"$eq": occasion}
    if article_type is not None: hard_filters["article_type"] = {"$eq": article_type}
    if color is not None: hard_filters["color"] = {"$eq": color}
    if brand_name is not None: hard_filters["brand_name"] = {"$eq": brand_name}
    if gender is not None: hard_filters["gender"] = {"$eq": gender}
    if is_jewellery is not None: hard_filters["is_jewellery"] = {"$eq": is_jewellery}
    if master_category is not None: hard_filters["master_category"] = {"$eq": master_category}
    if product_display_name is not None: hard_filters["product_display_name"] = {"$eq": product_display_name}
    if season is not None: hard_filters["season"] = {"$eq": season}
    if style_image is not None: hard_filters["style_image"] = {"$eq": style_image}
    if sub_category is not None: hard_filters["sub_category"] = {"$eq": sub_category}

    # if curr_category == 'topwear':
    #     hard_filters["sub_category"] = {"$eq": "topwear"}
    # if curr_category == 'bottomwear':
    #     hard_filters["sub_category"] = {"$eq": "bottomwear"}
    # if curr_category == 'footwear':
    #     hard_filters["master_category"] = {"$eq": "footwear"}
    # if curr_category == 'accessories':
    #     hard_filters["master_category"] = {"$eq": "accessories"}

    return hard_filters