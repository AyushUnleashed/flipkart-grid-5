import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from tqdm.auto import tqdm
from utils.pinecone_utils import setup_pinecone
import pickle
import chardet

def get_images(data):
    images = []
    for index, row in data.iterrows():
        try:
            # Download image from the 'link' column
            image_url = row['styleImage']
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

def insert_data(pinecone_index, model, bm25, data, images, batch_size=200):
    try:
        for i in tqdm(range(0, len(data), batch_size)):
            i_end = min(i+batch_size, len(data))
            data_batch = data.iloc[i:i_end]

            # change in columns being considered for meta_dict
            meta_dict = data_batch[['id', 'productDisplayName', 'brandName', 'masterCategory', 'subCategory', 'articleType', 'gender', 'baseColour', 'season', 'Occasion', 'isJewellery', 'styleImage']].to_dict(orient="records")
            print(data.columns)

            # narrowed down columns that need to be converted to strings and checked for 'none'
            cols_to_consider = ['productDisplayName', 'masterCategory', 'subCategory', 'baseColour', 'Pattern', 'Occasion', 'Sleeve styling', 'Sleeve length', 'Fabric', 'Neck']
            cols_for_pinecone_query = data_batch[cols_to_consider]
            pinecone_query_string = [ " ".join(str(val) for col, val in row.items() if val != 'none') for _, row in cols_for_pinecone_query.iterrows()]
            img_batch = images[i:i_end]

            # Create sparse BM25 vectors and dense vectors
            sparse_embeds = bm25.encode_documents([text for text in pinecone_query_string])
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

def upsert_csv(csv_file,char_enc, pinecone_index, model, bm25):
    try:
        data = pd.read_csv(csv_file, encoding=char_enc)
        data = data[['id', 'productDisplayName', 'brandName', 'baseColour','masterCategory', 'subCategory', 'articleType', 'gender', 'baseColour', 'season', 'Occasion', 'isJewellery', 'styleImage', 'Pattern', 'Occasion', 'Sleeve styling', 'Sleeve length', 'Fabric', 'Neck']] # use only specified columns
        images = get_images(data)
        # fit the bm25 model with the 'productDisplayName' column
        bm25.fit(data['productDisplayName'])

        # Serialize and save the fitted model
        with open('bm25.pkl', 'wb') as f:
            pickle.dump(bm25, f)

        insert_data(pinecone_index, model, bm25, data, images)

        # Show index description after uploading the documents
        pinecone_index.describe_index_stats()
    except Exception as e:
        print(f"Error occurred during upsert_csv: {e}")

def main():
    pinecone_index, model, bm25 = setup_pinecone()
    csv_file = "../dataset/top_100.csv"
    rawdata = open(csv_file, 'rb').read()
    result = chardet.detect(rawdata)
    char_enc = result['encoding']

    print(char_enc)
    upsert_csv(csv_file, char_enc, pinecone_index, model, bm25)

if __name__ == "__main__":
    main()