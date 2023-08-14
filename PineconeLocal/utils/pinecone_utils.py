import os
import pinecone
from pinecone_text.sparse import BM25Encoder
from sentence_transformers import SentenceTransformer
import torch

def initialize_pinecone():
    try:
        PINECONE_API_KEY = "dd4ed474-f906-4beb-9e87-c8808dfac671"
        PINECONE_ENVIRONMENT = "us-central1-gcp"
        # initialize connection to pinecone (get API key at app.pinecone.io)
        api_key = os.getenv("PINECONE_API_KEY") or PINECONE_API_KEY
        env = os.getenv("PINECONE_ENVIRONMENT") or PINECONE_ENVIRONMENT
        # init connection to pinecone
        pinecone.init(api_key=api_key, environment=env)
    except Exception as e:
        print(f"Error initializing Pinecone: {e}")



def create_index(index_name):
    try:
        if index_name not in pinecone.list_indexes():
            # create the index
            pinecone.create_index(
                index_name,
                dimension=512,
                metric="dotproduct",
                pod_type="s1"
            )
        return pinecone.Index(index_name)
    except Exception as e:
        print(f"Error creating index: {e}")

def setup_pinecone():
    try:
        initialize_pinecone()
        model, bm25 = get_clip_and_bm25_model()

        index_name = "grid-database"
        pinecone_index = create_index(index_name)
        return pinecone_index, model, bm25
    except Exception as e:
        print(f"Error setting up Pinecone: {e}")



def get_clip_and_bm25_model():
    try:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('sentence-transformers/clip-ViT-B-32', device=device)
        bm25 = BM25Encoder()
        return model, bm25
    except Exception as e:
        print(f"Error getting CLIP and BM25 model: {e}")

