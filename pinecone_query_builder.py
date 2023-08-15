from handle_user_prompt import get_prompt_insights
from handle_user_prompt import get_prompt
from userPreference import get_user_purchase_insight
from uniqueValues import brandName_array, baseColour_array, articleType_array,Occasion_array


def categorize_filters(insights, unique_array_dict):
    # Create dictionaries for hard and soft filters
    hard_filters = {"topwear": {}, "bottomwear": {}, "footwear": {}, "accessories": {}}
    soft_filters = {"topwear": {}, "bottomwear": {}, "footwear": {}, "accessories": {}}

    # Go through all 4 dictionaries
    for cat_insights in insights:
        category = cat_insights["category"]
        for key in ['baseColour', 'articleType', 'brandName', 'Occasion']:
            # Check if value exists in the corresponding unique array. If yes, it's a hard filter else a soft filter
            if cat_insights.get(key, None) and cat_insights[key] in unique_array_dict[key]:
                hard_filters[category][key] = cat_insights[key]
            elif cat_insights.get(key, None):
                soft_filters[category][key] = cat_insights[key]
    return hard_filters, soft_filters

# Unique values from PineconeLocal for 'brandName', 'baseColour', 'articleType', 'Occasion'
unique_array_dict = {"brandName": brandName_array, "baseColour": baseColour_array,
                     "articleType": articleType_array, "Occasion": Occasion_array}


# # For user's prompt insights
# user_prompt_insights = analyse_user_prompt_insights()
# hard_filters_prompt, soft_filters_prompt = categorize_filters(user_prompt_insights, unique_array_dict)

# keys = ['category', 'color', 'article_type', 'clothing_brand', 'occasion', 'other_info']
def analyse_user_bio_data():
    gender = "women"
    return gender

def analyse_user_purchase_insights():
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    user_purchase_insights = get_user_purchase_insight(user_purchase_csv)
    # top_wear, bottom_wear, foot_wear, accessories = user_purchase_insights
    print("user_purchase_insights:", user_purchase_insights)
    hard_filters_purchase, soft_filters_purchase = categorize_filters(user_purchase_insights, unique_array_dict)
    print("soft_filters_purchase:", soft_filters_purchase)
    print("hard_filters_purchase:", hard_filters_purchase)

# For user's purchase insights




def analyse_user_prompt_insights():
    user_prompt = get_prompt()
    top_wear, bottom_wear, foot_wear, accessories = get_prompt_insights(user_prompt=user_prompt)



if __name__ == "__main__":
    analyse_user_purchase_insights()
