import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from backend.utils import setup_pinecone
import pickle
import chardet
import time
import os

def get_images(data):
    images = []
    for index, row in data.iterrows():
        try:
            # Download image from the 'link' column
            image_url = row['style_image']
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

import concurrent.futures


# Define a function for parallel upsert
def parallel_upsert(index, upsert_data):
    index.upsert(upsert_data)

def insert_data_parallel(pinecone_index, model, bm25, data, batch_size=200, num_threads=20):
    try:
        total_batches = len(data) // batch_size + int(len(data) % batch_size != 0)
        print(f"Total batches: {total_batches}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []

            for batch_idx, i in enumerate(range(0, len(data), batch_size)):
                i_end = min(i + batch_size, len(data))
                data_batch = data.iloc[i:i_end]

                meta_dict = data_batch[['id', 'product_display_name', 'brand_name', 'master_category', 'sub_category', 'article_type', 'gender', 'color', 'season', 'occasion', 'is_jewellery', 'style_image']].to_dict(orient="records")

                cols_to_consider = ['product_display_name', 'master_category', 'sub_category', 'color', 'pattern', 'occasion', 'sleeve_styling', 'sleeve_length', 'fabric', 'neck']
                cols_for_pinecone_query = data_batch[cols_to_consider]
                pinecone_query_string = [" ".join(str(val) for col, val in row.items() if val != 'none') for _, row in cols_for_pinecone_query.iterrows()]
                
                # img_batch = images[i:i_end]
                
                img_batch = []
                for x in meta_dict: 
                    currImageId=x["id"]
                    currImageName=f'./downloaded_images2/{currImageId}.jpg'
                    if os.path.exists(currImageName):
                        # Open and display the image using PIL
                        img = Image.open(currImageName)
                        img_batch.append(img)
                    else:
                        print(f"The image '{currImageName}' does not exist in the {currImageName} directory.")

                '''
                go from index i to i_end
                get meta_dict["id"] as their image id
                find the imageId.jpg file in the local storage
                add such images in the img_batch array
                '''
                # for x in img_batch:
                #     print(type(x))
                #     print(x)

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

                futures.append(executor.submit(parallel_upsert, pinecone_index, upserts))

                # Print progress
                print(f"Batch {batch_idx + 1}/{total_batches}: Embeddings generated: {len(upserts)}")

                # Wait for all upsert tasks to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # This will raise an exception if an error occurs in the upsert
                except Exception as e:
                    print(f"Error upserting data: {e}")

    except Exception as e:
        print(f"Error inserting data: {e}")

# def insert_data(pinecone_index, model, bm25, data, images, batch_size=200):
#     try:
#         for i in tqdm(range(0, len(data), batch_size)):
#             i_end = min(i+batch_size, len(data))
#             data_batch = data.iloc[i:i_end]
#
#             # change in columns being considered for meta_dict
#             meta_dict = data_batch[['id', 'product_display_name', 'brand_name', 'master_category', 'sub_category', 'article_type', 'gender', 'color', 'season', 'occasion', 'is_jewellery', 'style_image']].to_dict(orient="records")
#             print(data.columns)
#
#             # narrowed down columns that need to be converted to strings and checked for 'none'
#             cols_to_consider = ['product_display_name', 'master_category', 'sub_category', 'color', 'pattern', 'occasion', 'sleeve_styling', 'sleeve_length', 'fabric', 'neck']
#             cols_for_pinecone_query = data_batch[cols_to_consider]
#             pinecone_query_string = [ " ".join(str(val) for col, val in row.items() if val != 'none') for _, row in cols_for_pinecone_query.iterrows()]
#             img_batch = images[i:i_end]
#
#             # Create sparse BM25 vectors and dense vectors
#             sparse_embeds = bm25.encode_documents([text for text in pinecone_query_string])
#             dense_embeds = model.encode(img_batch).tolist()
#
#             upserts = []
#             for sparse, dense, meta in zip(sparse_embeds, dense_embeds, meta_dict):
#                 upserts.append({
#                     'id': str(meta["id"]),
#                     'sparse_values': sparse,
#                     'values': dense,
#                     'metadata': meta,
#                 })
#
#             pinecone_index.upsert(upserts)
#     except Exception as e:
#         print(f"Error inserting data: {e}")

def upsert_csv(csv_file, char_enc, pinecone_index, model, bm25):
    try:
        total_start_time = time.time()  # Record the start time for the entire process

        # Timing point: Reading CSV
        read_csv_start_time = time.time()
        data = pd.read_csv(csv_file, encoding=char_enc)
        read_csv_end_time = time.time()
        read_csv_elapsed_time = read_csv_end_time - read_csv_start_time
        print("read_csv_elapsed_time:",read_csv_elapsed_time)
        data = data[['id', 'product_display_name', 'brand_name', 'color', 'master_category', 'sub_category', 'article_type', 'gender', 'season', 'occasion', 'is_jewellery', 'style_image', 'pattern', 'sleeve_styling', 'sleeve_length', 'fabric', 'neck']]
        # images = get_images(data)

        # Timing point: Fitting BM25 model
        bm25_fit_start_time = time.time()
        bm25.fit(data['product_display_name'])
        bm25_fit_end_time = time.time()
        bm25_fit_elapsed_time = bm25_fit_end_time - bm25_fit_start_time
        print("bm25_fit_elapsed_time:",bm25_fit_elapsed_time)

        with open('bm25_choli.pkl', 'wb') as f:
            pickle.dump(bm25, f)

        # Timing point: Upserts
        upsert_start_time = time.time()
        insert_data_parallel(pinecone_index, model, bm25, data, batch_size=200, num_threads=20)
        upsert_end_time = time.time()
        upsert_elapsed_time = upsert_end_time - upsert_start_time
        print("upsert_elapsed_time:",upsert_elapsed_time)

        pinecone_index.describe_index_stats()

        total_end_time = time.time()  # Record the end time for the entire process
        total_elapsed_time = total_end_time - total_start_time
        print("upsert_elapsed_time:",total_elapsed_time)

        # Print timing results
        print(f"Reading CSV took {read_csv_elapsed_time:.2f} seconds.")
        print(f"Fitting BM25 took {bm25_fit_elapsed_time:.2f} seconds.")
        print(f"Upserts took {upsert_elapsed_time:.2f} seconds.")
        print(f"Total time taken: {total_elapsed_time:.2f} seconds.")

    except Exception as e:
        print(f"Error occurred during upsert_csv: {e}")

def main():
    pinecone_index, model, bm25 = setup_pinecone()
    startTime=time.time()
    csv_file = "../dataset/choli.csv"
    rawdata = open(csv_file, 'rb').read()
    result = chardet.detect(rawdata)
    char_enc = result['encoding']

    print(char_enc)
    upsert_csv(csv_file, char_enc, pinecone_index, model, bm25)    
    endTime=time.time()
    print('final time to upsert',endTime-startTime)


if __name__ == "__main__":
    main()