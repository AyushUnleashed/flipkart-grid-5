import os
import pinecone
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from sentence_transformers import SentenceTransformer
import torch
from tqdm.auto import tqdm
from pinecone_text.sparse import BM25Encoder
from datasets import Dataset

class PineconeConnector:
    def __init__(self, api_key=None, environment=None):
        self.api_key = api_key or "fc0e7d98-b575-4842-9af2-619419ed1f50"
        self.environment = environment or "gcp-starter"
        pinecone.init(api_key=self.api_key, environment=self.environment)
    
    def create_index(self, index_name, dimension=512, metric="dotproduct", pod_type="s1"):
        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=dimension, metric=metric, pod_type=pod_type)
    
    def get_index(self, index_name):
        return pinecone.Index(index_name)
    
class DataProcessor:
    def __init__(self, csv_path, image_download=True):
        self.data = pd.read_csv(csv_path, encoding='utf-8')
        self.metadata = self.data.drop(columns=['year'])
        self.image_download = image_download
    
    def download_images(self):
        images = []
        for index, row in self.data.iterrows():
            image_url = row['link']
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                images.append(img)
            else:
                print(f"Failed to download image for index {index}")
        return images
    
    def prepare_metadata_strings(self):
        meta_batch = self.metadata.loc[:, ~self.metadata.columns.isin(['id', 'link'])].astype(str)
        meta_batch_strings = [" ".join(row) for row in meta_batch.values.tolist()]
        return meta_batch_strings

def main():
    api_key = os.getenv("PINECONE_API_KEY")
    environment = os.getenv("PINECONE_ENVIRONMENT")
    index_name = "grid-database"
    csv_path = "../Current-Data1.csv"
    
    pinecone_connector = PineconeConnector(api_key, environment)
    pinecone_connector.create_index(index_name)
    pinecone_index = pinecone_connector.get_index(index_name)
    
    data_processor = DataProcessor(csv_path)
    
    if data_processor.image_download:
        images = data_processor.download_images()
    
    bm25_encoder = BM25Encoder()
    bm25_encoder.fit(data_processor.metadata['productDisplayName'])
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('sentence-transformers/clip-ViT-B-32', device=device)
    
    batch_size = 200
    for i in tqdm(range(0, len(data_processor.data), batch_size)):
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

if __name__ == "__main__":
    main()
