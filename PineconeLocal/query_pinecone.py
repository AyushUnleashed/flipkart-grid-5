from utils.pinecone_utils import setup_pinecone
import pickle

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


def perform_query(pinecone_index, bm25, model, query, alpha=0.05, top_k=14):
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
    )
    return result


def query_pinecone(query, pinecone_index, model, bm25):
    result = perform_query(pinecone_index, bm25, model, query)

    print(result["matches"])
    for x in result["matches"]:
        print(x["metadata"]['productDisplayName'])
        print(x["metadata"]['link'])
        print("\n")


def main():
    bm25_fname = "bm25.pkl"
    pinecone_index, model, bm25 = setup_pinecone()
    # load the fitted bm25 model
    with open(bm25_fname, 'rb') as f:
        bm25 = pickle.load(f)
    query = "Peter England baby blue jeans for men"
    query_pinecone(query, pinecone_index, model, bm25)

if __name__ == "__main__":
    main()