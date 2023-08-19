from get_filters_from_insights import analyse_user_prompt_insights, analyse_user_purchase_insights_simple, \
    categorize_filters, unique_array_dict
from prompt_insights import get_prompt
from PineconeLocal.utils.filters import build_hard_filters
from PineconeLocal.query_pinecone import run_pinecone_query

def pre_process_filters(user_prompt, user_purchase_csv, change_prompt_insights=None, change_prompt=False):
    if change_prompt:
        hard_filters_prompt, soft_filters_prompt = categorize_filters(change_prompt_insights, unique_array_dict)
    else:
        hard_filters_prompt, soft_filters_prompt = analyse_user_prompt_insights(user_prompt)

    pinecone_queries_purchase = analyse_user_purchase_insights_simple(user_purchase_csv)
    # hard_filters_purchase, soft_filters_purchase = analyse_user_purchase_insights(user_purchase_csv)

    hard_filters_to_be_used = process_hard_filters(hard_filters_prompt)
    pinecone_filters = generate_pinecone_metadata_filters(hard_filters_to_be_used)
    pinecone_queries = process_soft_filters(soft_filters_prompt)
    return pinecone_filters, pinecone_queries, pinecone_queries_purchase

def process_soft_filters(soft_filters):
    categories = ["topwear", "bottomwear", "footwear", "accessories"]
    pinecone_queries = []

    for category in categories:
        category_data = soft_filters.get(category, {})
        pinecone_query = ""

        for key, value in category_data.items():
            if key != 'category' and value != 'none':
                if pinecone_query:
                    pinecone_query += ' '
                pinecone_query += value

        pinecone_queries.append(pinecone_query)

    return pinecone_queries

def process_hard_filters(hard_filters_prompt):
    categories = ["topwear", "bottomwear", "footwear", "accessories"]

    hard_filters_to_be_used = {}

    for category in categories:
        #purchase_category_filters = hard_filters_purchase.get(category, {})
        prompt_category_filters = hard_filters_prompt.get(category, {})

        # Check if any value (except 'category') is not 'none' in the purchase_category_filters
        if any(value != 'none' and key != 'category' for key, value in prompt_category_filters.items()):
            hard_filters_to_be_used[category] = prompt_category_filters



    return hard_filters_to_be_used

def generate_pinecone_metadata_filters(hard_filters_to_be_used):
    categories = ["topwear", "bottomwear", "footwear", "accessories"]
    filters = {}

    for category in categories:
        if category in hard_filters_to_be_used:
            filter_data = hard_filters_to_be_used[category]
            filters[category] = build_hard_filters(
                occasion=None if filter_data.get('occasion') == 'none' else filter_data.get('occasion'),
                article_type=None if filter_data.get('article_type') == 'none' else filter_data.get('article_type'),
                color=None if filter_data.get('color') == 'none' else filter_data.get('color'),
                brand_name=None if filter_data.get('brand_name') == 'none' else filter_data.get('brand_name'),
                gender=None,
                is_jewellery=None,
                master_category=None,
                product_display_name=None,
                season=None,
                style_image=None,
                sub_category=None
            )

    return filters




def process_category(category,index, filters, queries, queries_purchase):
    print("\nProcessing category:", category)
    category_filters = filters.get(category, {})
    category_query = queries[index]

    if not category_filters and not category_query:
        category_query = queries_purchase[index]

    if not category_query:
        category_query = category

    print("Category Filters:")
    print(category_filters)
    print("Category Query:")
    print(category_query)

    category_outfit = run_pinecone_query(category_query, category_filters)
    print("\nGenerated Outfit for", category, "is:", category_outfit)
    print("\n--------------------------\n")
    return category_outfit

def get_outfit_from_prompt(user_prompt, user_purchase_csv):
    pinecone_filters, pinecone_queries, pinecone_queries_purchase = pre_process_filters(user_prompt, user_purchase_csv)
    print("pinecone_filters:", pinecone_filters)
    print("pinecone_queries", pinecone_queries)
    print("pinecone_queries_purchase", pinecone_queries_purchase)

    outfit = []
    categories = ["topwear","bottomwear","footwear","accessories"]
    for index, category in enumerate(categories):
        category_outfit = process_category(category, index, pinecone_filters, pinecone_queries, pinecone_queries_purchase)
        outfit.append(category_outfit)

    print("\n\n **************\n\n")
    print("\n Generated Outfit is: ")
    print("\n -------------------------")
    print("\noutfit:\n", outfit)
    print("\n -------------------------")
    return outfit

def get_outfit_selected(user_prompt, user_purchase_csv,curr_categories, category_dict_array):
    # add None if we don't want to fetch new one

    pinecone_filters, pinecone_queries, pinecone_queries_purchase = pre_process_filters(user_prompt, user_purchase_csv,category_dict_array,change_prompt=True)
    outfit = []
    for index, category in enumerate(curr_categories):
        if category == 'none':
            outfit.append(None)
            continue

        category_outfit = process_category(category, index, pinecone_filters, pinecone_queries, pinecone_queries_purchase)
        outfit.append(category_outfit)
    return outfit





if __name__ == "__main__":
    user_prompt = get_prompt()
    user_purchase_csv = 'dataset/user_history_data/gwen_2.csv'
    get_outfit_from_prompt(user_prompt,user_purchase_csv)