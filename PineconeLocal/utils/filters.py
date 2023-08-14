
def build_hard_filters(occasion=None, articleType=None, baseColor=None, brandName=None,
                       gender=None, isJewellery=None, masterCategory=None,
                       productDisplayName=None, season=None, styleImage=None,
                       subCategory=None):
    hard_filters = {}

    if occasion is not None: hard_filters["Occasion"] = {"$eq": occasion}
    if articleType is not None: hard_filters["articleType"] = {"$eq": articleType}
    if baseColor is not None: hard_filters["baseColor"] = {"$eq": baseColor}
    if brandName is not None: hard_filters["brandName"] = {"$eq": brandName}
    if gender is not None: hard_filters["gender"] = {"$eq": gender}
    if isJewellery is not None: hard_filters["isJewellery"] = {"$eq": isJewellery}
    if masterCategory is not None: hard_filters["masterCategory"] = {"$eq": masterCategory}
    if productDisplayName is not None: hard_filters["productDisplayName"] = {"$eq": productDisplayName}
    if season is not None: hard_filters["season"] = {"$eq": season}
    if styleImage is not None: hard_filters["styleImage"] = {"$eq": styleImage}
    if subCategory is not None: hard_filters["subCategory"] = {"$eq": subCategory}

    return hard_filters