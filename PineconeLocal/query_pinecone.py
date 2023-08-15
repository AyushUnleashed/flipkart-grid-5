from utils.pinecone_utils import setup_pinecone
import pickle
from utils.filters import build_hard_filters
def hybrid_scale(dense, sparse, alpha: float):
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    # scale sparse and dense vectors to create hybrid search vecs
    hsparse = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse


def perform_query(pinecone_index, bm25, model, query, hard_filters, alpha=0.05, top_k=14):
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
    result = perform_query(pinecone_index, bm25, model, query, hard_filters=hard_filters)

    print(result["matches"])
    for x in result["matches"]:
        print(x["metadata"]['productDisplayName'])
        print(x["metadata"]['styleImage'])
        print("\n")


def main():
    bm25_fname = "bm25.pkl"
    pinecone_index, model, bm25 = setup_pinecone()
    # load the fitted bm25 model
    with open(bm25_fname, 'rb') as f:
        bm25 = pickle.load(f)
    query = "Peter England baby blue jeans for men"
    query = "locomotive jeans"
    hard_filters = build_hard_filters(articleType="sports_shoes", baseColor="silver", brandName="reebok", gender="men")
    query_pinecone(query, pinecone_index, model, bm25, hard_filters)

if __name__ == "__main__":
    main()