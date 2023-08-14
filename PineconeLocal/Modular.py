import os
import pinecone
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from sentence_transformers import SentenceTransformer
from pinecone_text.sparse import BM25Encoder
from tqdm.auto import tqdm

# Connect to Pinecone
def connect_to_pinecone():
    api_key = os.getenv("PINECONE_API_KEY") or "fc0e7d98-b575-4842-9af2-619419ed1f50"
    env = os.getenv("PINECONE_ENVIRONMENT") or "gcp-starter"
    pinecone.init(api_key=api_key, environment=env)

# Initialize Index
def initialize_index(index_name):
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            index_name,
            dimension=512,
            metric="dotproduct",
            pod_type="s1"
        )

# Load CSV data and Images
def load_data_and_images(csv_path):
    data = pd.read_csv(csv_path, encoding='utf-8')
    metadata = data.drop(columns=['year'])
    images = []

    for index, row in data.iterrows():
        image_url = row['link']
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            images.append(img)
        else:
            print(f"Failed to download image for index {index}")

    return metadata, images

# Create Sparse Vectors using BM25
def create_sparse_vectors(metadata):
    bm25 = BM25Encoder()
    bm25.fit(metadata['productDisplayName'])
    sparse_embeds = bm25.encode_documents(metadata['productDisplayName'])
    return sparse_embeds

# Create Dense Vectors using CLIP
def create_dense_vectors(images):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer(
        'sentence-transformers/clip-ViT-B-32',
        device=device
    )
    dense_embeds = model.encode(images).tolist()
    return dense_embeds

# Upsert Documents to Pinecone Index
def upsert_documents(index, metadata, images, batch_size=200):
    for i in tqdm(range(0, len(metadata), batch_size)):
        i_end = min(i + batch_size, len(metadata))
        meta_batch = metadata.iloc[i:i_end]
        img_batch = images[i:i_end]
        sparse_embeds = create_sparse_vectors(meta_batch)
        dense_embeds = create_dense_vectors(img_batch)
        upserts = []

        for sparse, dense, meta in zip(sparse_embeds, dense_embeds, meta_batch.to_dict(orient="records")):
            upserts.append({
                'id': str(meta["id"]),
                'sparse_values': sparse,
                'values': dense,
                'metadata': meta
            })

        index.upsert(upserts)

def main():
    index_name = "hybrid-image-search"
    csv_path = "./Current-Data.csv"

    connect_to_pinecone()
    initialize_index(index_name)
    pinecone_index = pinecone.Index(index_name)

    metadata, images = load_data_and_images(csv_path)
    upsert_documents(pinecone_index, metadata, images)

if __name__ == "__main__":
    main()
