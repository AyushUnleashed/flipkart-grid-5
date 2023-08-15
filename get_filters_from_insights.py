from prompt_insights import get_prompt_insights
from prompt_insights import get_prompt
from user_purchase_insights import get_user_purchase_insight
from utils.uniqueValues import brand_name_array, color_array, article_type_array,occasion_array


def categorize_filters(insights, unique_array_dict):
    # Create dictionaries for hard and soft filters
    hard_filters = {"topwear": {}, "bottomwear": {}, "footwear": {}, "accessories": {}}
    soft_filters = {"topwear": {}, "bottomwear": {}, "footwear": {}, "accessories": {}}

    # Go through all 4 dictionaries
    for cat_insights in insights:
        category = cat_insights["category"]
        # Add the 'category' key to the hard & soft filters insights
        hard_filters[category]['category'] = category
        soft_filters[category]['category'] = category
        soft_filters[category]['other_info'] = cat_insights['other_info']

        for key in ['color', 'article_type', 'brand_name', 'occasion']:
            # Check if value exists in the corresponding unique array. If yes, it's a hard filter else a soft filter
            if cat_insights.get(key, None) and cat_insights[key] in unique_array_dict[key]:
                hard_filters[category][key] = cat_insights[key]
                soft_filters[category][key] = 'none'
            elif cat_insights.get(key, None):
                soft_filters[category][key] = cat_insights[key]
                hard_filters[category][key] = 'none'
    return hard_filters, soft_filters

# Unique values from PineconeLocal for 'brandName', 'baseColour', 'articleType', 'Occasion'
unique_array_dict = {"brand_name": brand_name_array, "color": color_array,
                     "article_type": article_type_array, "occasion": occasion_array}


# # For user's prompt insights
# user_prompt_insights = analyse_user_prompt_insights()
# hard_filters_prompt, soft_filters_prompt = categorize_filters(user_prompt_insights, unique_array_dict)

# keys = ['category', 'color', 'article_type', 'clothing_brand', 'occasion', 'other_info']
def analyse_user_bio_data():
    gender = "women"
    return gender

# def analyse_user_purchase_insights(user_purchase_csv):
#     user_purchase_insights = get_user_purchase_insight(user_purchase_csv)
#     # top_wear, bottom_wear, foot_wear, accessories = user_purchase_insights
#     print("user_purchase_insights:", user_purchase_insights)
#     hard_filters_purchase, soft_filters_purchase = categorize_filters(user_purchase_insights, unique_array_dict)
#     print("soft_filters_purchase:", soft_filters_purchase)
#     print("hard_filters_purchase:", hard_filters_purchase)
#     return hard_filters_purchase, soft_filters_purchase
# # For user's purchase insights


def analyse_user_purchase_insights_simple(user_purchase_csv):
    user_purchase_insights = get_user_purchase_insight(user_purchase_csv)
    categories = ["topwear", "bottomwear", "footwear", "accessories"]
    pinecone_queries = []

    for i, category in enumerate(categories, start=0):
        category_data = user_purchase_insights[i]
        pinecone_query = ""

        for key, value in category_data.items():
            if key != 'category' and value != 'none':
                if pinecone_query:
                    pinecone_query += ' '
                pinecone_query += value

        pinecone_queries.append(pinecone_query)

    return pinecone_queries

def analyse_user_prompt_insights(user_prompt):

    top_wear, bottom_wear, foot_wear, accessories = get_prompt_insights(user_prompt=user_prompt)
    user_prompt_insights = [top_wear, bottom_wear, foot_wear, accessories]
    print("user_prompt_insights:", user_prompt_insights)

    hard_filters_prompt, soft_filters_prompt = categorize_filters(user_prompt_insights, unique_array_dict)
    print("soft_filters_prompt:", soft_filters_prompt)
    print("hard_filters_prompt:", hard_filters_prompt)
    return hard_filters_prompt, soft_filters_prompt


if __name__ == "__main__":
    print("\n\nuser_purchase_insights:::: ")
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    analyse_user_purchase_insights_simple(user_purchase_csv)
    print("\n\n***************************\n")
    print("\n\nuser_prompt_insights:::: ")
    user_prompt = get_prompt()
    #analyse_user_prompt_insights(user_prompt)
    print("\n\n***************************")
