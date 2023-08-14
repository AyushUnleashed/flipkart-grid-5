import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from tqdm.auto import tqdm
from utils.pinecone_utils import setup_pinecone
import pickle

def get_images(data):
    images = []
    for index, row in data.iterrows():
        try:
            # Download image from the 'link' column
            image_url = row['link']
            response = requests.get(image_url)

            if response.status_code == 200:
                # Convert the downloaded content into a PIL image
                img = Image.open(BytesIO(response.content))
                images.append(img)
            else:
                print(f"Failed to download image for index {index}")
        except Exception as e:
            print(f"Error encountered while processing image at index {index}. Error: {e}")
    return images

def insert_data(pinecone_index, model, bm25, metadata, images, batch_size=200):
    try:
        for i in tqdm(range(0, len(metadata), batch_size)):
            i_end = min(i+batch_size, len(metadata))
            meta_batch = metadata.iloc[i:i_end]
            meta_dict = meta_batch.to_dict(orient="records")

            # Convert all columns (except 'id' and 'link') to strings
            meta_batch = meta_batch.loc[:, ~meta_batch.columns.isin(['id', 'link'])].astype(str)

            meta_batch_strings = [" ".join(row) for row in meta_batch.values.tolist()]

            img_batch = images[i:i_end]

            # Create sparse BM25 vectors and dense vectors
            sparse_embeds = bm25.encode_documents([text for text in meta_batch_strings])
            dense_embeds = model.encode(img_batch).tolist()

            upserts = []
            for sparse, dense, meta in zip(sparse_embeds, dense_embeds, meta_dict):
                upserts.append({
                    'id': str(meta["id"]),
                    'sparse_values': sparse,
                    'values': dense,
                    'metadata': meta,
                })

            pinecone_index.upsert(upserts)
    except Exception as e:
        print(f"Error inserting data: {e}")

def upsert_csv(csv_file, pinecone_index, model, bm25):
    try:
        data = pd.read_csv(csv_file, encoding='utf-8')
        metadata = data.drop(columns=['year'])
        images = get_images(data)

        # fit the bm25 model with the entire corpus
        bm25.fit(metadata['productDisplayName'])

        # Serialize and save the fitted model
        with open('bm25.pkl', 'wb') as f:
            pickle.dump(bm25, f)

        insert_data(pinecone_index, model, bm25, metadata, images)

        # Show index description after uploading the documents
        pinecone_index.describe_index_stats()
    except Exception as e:
        print(f"Error occurred during upsert_csv: {e}")


def main():
    pinecone_index, model, bm25 = setup_pinecone()
    csv_file = "./Current-Data1.csv"
    upsert_csv(csv_file, pinecone_index, model, bm25)

if __name__ == "__main__":
    main()