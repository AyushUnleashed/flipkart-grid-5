
from pre_process_hard_filters import call_for_individual_categories, pre_process_filters

def main(user_prompt):
    user_purchase_csv = 'dataset/user_history_data/gwen.csv'
    pinecone_filters, pinecone_queries, pinecone_queries_purchase = pre_process_filters(user_prompt,user_purchase_csv)
    print("pinecone_filters:",pinecone_filters)
    print("pinecone_queries",pinecone_queries)
    print("pinecone_queries_purchase", pinecone_queries_purchase)
    outfit = call_for_individual_categories(pinecone_filters, pinecone_queries, pinecone_queries_purchase)
    print("\noutfit is: \n",outfit)

if __name__ == "__main__":

    while True:
        user_prompt = input("Enter outfit description:")
        if(user_prompt == ""):
            print("user prompt cannot be empty\n")
            continue

        main(user_prompt=user_prompt)
