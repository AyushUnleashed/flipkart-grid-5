import os
import pinecone
from pinecone_text.sparse import BM25Encoder
from sentence_transformers import SentenceTransformer
import torch
import time
from dotenv import find_dotenv, load_dotenv
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

def initialize_pinecone():
    try:
        # initialize connection to pinecone (get API key at app.pinecone.io)
        api_key = os.getenv("PINECONE_API_KEY")
        env = os.getenv("PINECONE_ENVIRONMENT")
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
    start_time = time.time()

    try:
        print('Initializing Pinecone...')
        initialize_pinecone()
        print('Initialization completed.')

        print('Getting CLIP and BM25 model...')
        model, bm25 = get_clip_and_bm25_model()
        print('Models obtained:')
        print('---- Model:', model)
        print('---- BM25:', bm25)

        print('Creating index...')
        index_name = "final-database"
        pinecone_index = create_index(index_name)
        print('Index created:', pinecone_index)
        print('Setup completed.')
        end_time = time.time()
        print(f'Time taken: {end_time - start_time} seconds')
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

