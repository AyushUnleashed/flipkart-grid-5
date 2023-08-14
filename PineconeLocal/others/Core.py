import os
import pinecone

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = os.getenv("PINECONE_API_KEY") or "fc0e7d98-b575-4842-9af2-619419ed1f50"
# find your environment next to the api key in pinecone console
env = os.getenv("PINECONE_ENVIRONMENT") or "gcp-starter"

# init connection to pinecone
pinecone.init(
    api_key=api_key,
    environment=env
)
index_name = "grid-database"

if index_name not in pinecone.list_indexes():
    # create the index
    pinecone.create_index(
      index_name,
      dimension=512,
      metric="dotproduct",
      pod_type="s1"
    )

pinecone_index = pinecone.Index(index_name)

import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datasets import Dataset

# Load CSV data into a Pandas DataFrame
csv_path = "../Current-Data1.csv"
data = pd.read_csv(csv_path,encoding='utf-8')

metadata = data.drop(columns=['year'])

images = []

# Loop through each row in the DataFrame
for index, row in data.iterrows():
    # Download image from the 'link' column
    image_url = row['link']
    response = requests.get(image_url)
    if response.status_code == 200:
        # Convert the downloaded content into a PIL image
        img = Image.open(BytesIO(response.content))
        images.append(img)
    else:
        print(f"Failed to download image for index {index}")

images[5]

from pinecone_text.sparse import BM25Encoder

bm25 = BM25Encoder()

"Turtle Check Men Navy Blue Shirt".lower().split()


bm25.fit(metadata['productDisplayName'])

metadata['productDisplayName'][0]

bm25.encode_queries(metadata['productDisplayName'][0])

bm25.encode_documents(metadata['productDisplayName'][0])

from sentence_transformers import SentenceTransformer
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# load a CLIP model from huggingface
model = SentenceTransformer(
    'sentence-transformers/clip-ViT-B-32',
    device=device
)
model


dense_vec = model.encode([metadata['productDisplayName'][0]])
dense_vec.shape

from tqdm.auto import tqdm
# print(type(pinecone_index))
batch_size = 200
# len(data)
for i in tqdm(range(0, len(data), batch_size)):
    # find end of batch
    
    i_end = min(i+batch_size, len(data))
    # extract metadata batch
    print('ending varaible', i_end)
   
    meta_batch = metadata.iloc[i:i_end]
    meta_dict = meta_batch.to_dict(orient="records")
  
    print('the dict is this\n', meta_dict)
    print('length of the dict\n', len(meta_dict))
    # concatinate all metadata field except for id and year to form a single string
    # meta_batch_text = [" ".join(row) for row in meta_batch.values.tolist()]
    # meta_batch = [" ".join(x) for x in meta_batch.loc[:, ~meta_batch.columns.isin(['id', 'link'])].values.tolist()]


    # Convert all columns (except 'id' and 'link') to strings
    meta_batch = meta_batch.loc[:, ~meta_batch.columns.isin(['id', 'link'])].astype(str)

    # Join the values in each row into a single string
    meta_batch_strings = [" ".join(row) for row in meta_batch.values.tolist()]
    # print('the string which is being uploaded to pinecone for sparse vector \n', meta_batch_strings);
    # # meta_batch_text = [" ".join(str(value) for value in row) for row in meta_batch.values.tolist()]
    # # extract image batch
    # print('meta dictionary \n', meta_dict)

        


    img_batch = images[i:i_end]
    print('the dense is this\n', len(images))
    
    # create sparse BM25 vectors
    sparse_embeds = bm25.encode_documents([text for text in meta_batch_strings])
    print('the sparse is this\n', len(sparse_embeds))
    # create dense vectors
    dense_embeds = model.encode(img_batch).tolist()
    print('the dense is this\n', len(dense_embeds))
    
    # create unique IDs
    # ids = [str(x) for x in range(i, i_end)]
    # for x in ids:
    #     print(ids[int(x)])

    upserts = []
    # loop through the data and create dictionaries for uploading documents to pinecone index
    for sparse, dense, meta in zip(sparse_embeds, dense_embeds, meta_dict):
        upserts.append({
            'id': str(meta["id"]),
            'sparse_values': sparse,
            'values': dense,
            'metadata': meta
        })
    # upload the documents to the new hybrid index
    print('length of upserts: \n', len(upserts))
    pinecone_index.upsert(upserts)
    # print(index)
    # print(type(pinecone_index))


# show index description after uploading the documents
pinecone_index.describe_index_stats()

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


query = "Peter England baby blue jeans for men"
sparse = bm25.encode_queries(query)
dense = model.encode(query).tolist()
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.05)
# search
result = pinecone_index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
print(result["matches"])

for x in result["matches"]:
    print(x["metadata"]['productDisplayName'])
