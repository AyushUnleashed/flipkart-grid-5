from get_filters_from_insights import analyse_user_prompt_insights, analyse_user_purchase_insights_simple
from prompt_insights import get_prompt
from PineconeLocal.utils.filters import build_hard_filters
from PineconeLocal.query_pinecone import run_pinecone_query

def pre_process_filters(user_prompt, user_purchase_csv):
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




def call_for_individual_categories(pinecone_filters, pinecone_queries, pinecone_queries_purchase):
    # Generate Pinecone metadata filters

    # Separate variables for each category's filters
    topwear_pinecone_filters = pinecone_filters.get('topwear', {})
    bottomwear_pinecone_filters = pinecone_filters.get('bottomwear', {})
    footwear_pinecone_filters = pinecone_filters.get('footwear', {})
    accessories_pinecone_filters = pinecone_filters.get('accessories', {})
    # Check and update queries for each category
    if not topwear_pinecone_filters and not pinecone_queries[0]:
        pinecone_queries[0] = pinecone_queries_purchase[0]

    if not bottomwear_pinecone_filters and not pinecone_queries[1]:
        pinecone_queries[1] = pinecone_queries_purchase[1]

    if not footwear_pinecone_filters and not pinecone_queries[2]:
        pinecone_queries[2] = pinecone_queries_purchase[2]

    if not accessories_pinecone_filters and not pinecone_queries[3]:
        pinecone_queries[3] = pinecone_queries_purchase[3]

    # Add the following lines to handle empty queries array
    if not pinecone_queries[0]:
        pinecone_queries[0] = 'topwear'
    if not pinecone_queries[1]:
        pinecone_queries[1] = 'bottomwear'
    if not pinecone_queries[2]:
        pinecone_queries[2] = 'footwear'
    if not pinecone_queries[3]:
        pinecone_queries[3] = 'accessories'

        # Separate variables for each category's queries
    topwear_pinecone_query = pinecone_queries[0]
    bottomwear_pinecone_query = pinecone_queries[1]
    footwear_pinecone_query = pinecone_queries[2]
    accessories_pinecone_query = pinecone_queries[3]


    # Print filters and queries for each category
    print("Topwear Filters:")
    print(topwear_pinecone_filters)
    print("Topwear Query:")
    print(topwear_pinecone_query)

    print("\nBottomwear Filters:")
    print(bottomwear_pinecone_filters)
    print("Bottomwear Query:")
    print(bottomwear_pinecone_query)

    print("\nFootwear Filters:")
    print(footwear_pinecone_filters)
    print("Footwear Query:")
    print(footwear_pinecone_query)

    print("\nAccessories Filters:")
    print(accessories_pinecone_filters)
    print("Accessories Query:")
    print(accessories_pinecone_query)


    first_topwear = run_pinecone_query(topwear_pinecone_query, topwear_pinecone_filters)
    first_bottomwear = run_pinecone_query(bottomwear_pinecone_query,bottomwear_pinecone_filters)
    first_footwear = run_pinecone_query(footwear_pinecone_query, footwear_pinecone_filters)
    first_accessory = run_pinecone_query(accessories_pinecone_query, accessories_pinecone_filters)

    print("\n\n\n **************\n\n\n")
    print("\n Generated Outfit is: ")
    print("\n -------------------------")
    print("\nfirst_topwear:\n",first_topwear)
    print("\nfirst_bottomwear:\n",first_bottomwear)
    print("\nfirst_footwear:\n",first_footwear)
    print("\nfirst_accessory:\n",first_accessory)
    print("\n -------------------------")
    outfit = [first_topwear, first_bottomwear, first_footwear, first_accessory]
    return outfit


def main(user_prompt):
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    pinecone_filters, pinecone_queries, pinecone_queries_purchase = pre_process_filters(user_prompt,user_purchase_csv)
    print("pinecone_filters:",pinecone_filters)
    print("pinecone_queries",pinecone_queries)
    print("pinecone_queries_purchase", pinecone_queries_purchase)
    call_for_individual_categories(pinecone_filters, pinecone_queries, pinecone_queries_purchase)


if __name__ == "__main__":
    user_prompt = get_prompt()
    main(user_prompt)
