from PineconeLocal.utils.pinecone_utils import setup_pinecone
import pickle
from PineconeLocal.utils.filters import build_hard_filters
import os
from PineconeLocal.utils.user_bio_data.userBio import current_user_bio_data
import random

def hybrid_scale(dense, sparse, alpha: float):
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    # scale sparse and dense vectors to create hybrid search vecs
    hsparse = {
        'indices': sparse['indices'],
        'values': [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse


def get_bio_data(hard_filters):
    hard_filters['gender'] = {"$in": ["unisex", current_user_bio_data.gender]}
    print(hard_filters)
    return hard_filters


def perform_query(pinecone_index, bm25, model, query, hard_filters, top_k=5, alpha=0.05):

    hard_filters = get_bio_data(hard_filters=hard_filters)
    sparse = bm25.encode_queries(query)
    dense = model.encode(query).tolist()
    # scale sparse and dense vectors
    hdense, hsparse = hybrid_scale(dense, sparse, alpha)
    # search
    result = pinecone_index.query(
        top_k=top_k,
        vector=hdense,
        sparse_vector=hsparse,
        include_metadata=True,
        filter=hard_filters
    )
    return result


def query_pinecone(query, pinecone_index, model, bm25, hard_filters):
    top_k = 5
    result = perform_query(pinecone_index, bm25, model, query, hard_filters=hard_filters, top_k=top_k)

    print("Result of pinecone query for query:", query, "\n\n")
    print(result["matches"])
    if len(result["matches"]) > 0:
        #selected_item  = result["matches"][0]["metadata"]
        selected_item = random.choice(result["matches"])["metadata"]
    else:
        selected_item  = {}
    # for x in result["matches"]:
    #     print(x["metadata"]['product_display_name'])
    #     print(x["metadata"]['style_image'])
    #     print("\n")

    return selected_item


pinecone_index, model, bm25 = setup_pinecone()


def run_pinecone_query(query, hard_filters):
    bm25_fname = os.path.join(os.path.dirname(__file__), 'bm25.pkl')

    # pinecone_index, model, bm25 = setup_pinecone()
    # load the fitted bm25 model
    with open(bm25_fname, 'rb') as f:
        bm25 = pickle.load(f)
    return query_pinecone(query, pinecone_index, model, bm25, hard_filters)


def main():
    query = "Peter England baby blue jeans"
    # query = "locomotive jeans"
    hard_filters = build_hard_filters(color="blue", brand_name="peter_england")
    run_pinecone_query(query, hard_filters)


if __name__ == "__main__":
    main()
