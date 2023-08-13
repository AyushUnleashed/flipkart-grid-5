# %% [markdown]
# [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pinecone-io/examples/blob/master/learn/search/hybrid-search/ecommerce-search/ecommerce-search.ipynb) [![Open nbviewer](https://raw.githubusercontent.com/pinecone-io/examples/master/assets/nbviewer-shield.svg)](https://nbviewer.org/github/pinecone-io/examples/blob/master/learn/search/hybrid-search/ecommerce-search/ecommerce-search.ipynb)
# 
# # Hybrid Search for E-Commerce with Pinecone

# %% [markdown]
# 
# Hybrid vector search is combination of traditional keyword search and modern dense vector search. It has emerged as a powerful tool for e-commerce companies looking to improve the search experience for their customers.
# 
# By combining the strengths of traditional text-based search algorithms with the visual recognition capabilities of deep learning models, hybrid vector search allows users to search for products using a combination of text and images. This can be especially useful for product searches, where customers may not know the exact name or details of the item they are looking for.
# 
# Pinecone's new **sparse-dense index** allows you to seamlessly perform hybrid search for e-commerce or in any other context. This notebook demonstrates how to use the new hybrid search feature to improve e-commerce search.

# %% [markdown]
# ## Install Dependencies

# %% [markdown]
# First, let's import the necessary libraries
# 

# %%
!pip install -qU datasets transformers sentence-transformers \
                 pinecone-client pinecone-text protobuf==3.20.3
%pip install pandas requests Pillow datasets


# %% [markdown]
# ## Connect to Pinecone

# %% [markdown]
# Let's initiate a connection and create an index. For this, we need a [free API key](https://app.pinecone.io/), and then we initialize the connection like so:

# %%
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

# %% [markdown]
# To use the `sparse-dense` index in Pinecone we must set `metric="dotproduct"` and use either `s1` or `p1` pods. We also align the `dimension` value to that of our retrieval model, which outputs `512`-dimensional vectors.

# %%
# choose a name for your index
index_name = "hybrid-image-search"

if index_name not in pinecone.list_indexes():
    # create the index
    pinecone.create_index(
      index_name,
      dimension=512,
      metric="dotproduct",
      pod_type="s1"
    )

# %% [markdown]
# Now we have created the sparse-dense enabled index, we connect to it:

# %%
index = pinecone.Index(index_name)

# %% [markdown]
# *Note: we are using `GRPCIndex` rather than `Index` for the improved upsert speeds, either can be used with the sparse-dense index.*

# %% [markdown]
# # Load Dataset

# %% [markdown]
# We will work with a subset of the [Open Fashion Product Images](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small) dataset, consisting of ~44K fashion products with images and category labels describing the products. The dataset can be loaded from the Huggigface Datasets hub as follows:

# %%
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from datasets import Dataset

# Load CSV data into a Pandas DataFrame
csv_path = "./Current-Data.csv"
data = pd.read_csv(csv_path,encoding='utf-8')

# Display the first few rows of the DataFrame
# data

# print(len(data))

# from datasets import load_dataset

# # load the dataset from huggingface datasets hub
# fashion = load_dataset(
#     "ashraq/fashion-product-images-small",
#     split="train"
# )
# fashion


# from datasets import load_dataset

# # load the dataset from huggingface datasets hub
# fashion = load_dataset("csv", data_files="/content/sample_data/Training_Pinecone.csv", delimiter="\t", column_names=["id","gender","masterCategory","subCategory","articleType","baseColour","season","year","usage","productDisplayName","link"], split="train", )
# fashion

# %% [markdown]
# We will first assign the images and metadata into separate variables and then convert the metadata into a pandas dataframe.

# %%
metadata = data.drop(columns=['link', 'id', 'year'])
# Convert metadata to a Pandas DataFrame
# metadata = metadata.to_pandas()

# Initialize empty list to store images
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

# Now you can work directly with 'metadata' Pandas DataFrame and 'images' list
# For example:
# print(metadata.head())
# for column in metadata.columns:
#     if metadata[column].dtype == 'object':
#         try:
#             pd.to_numeric(metadata[column], errors='raise')
#             print(f"{column} might contain numeric data (including floats).")
#         except:
#             print(f"{column} likely contains non-numeric data (including strings).")
#     else:
#         print(f"{column} has data type {metadata[column].dtype}.")


# %%
images[5]

# %% [markdown]
# We need both sparse and dense vectors to perform hybrid search. We will use all the metadata fields except for the `id` and `year` to create sparse vectors and the product images to create dense vectors.

# %% [markdown]
# ## Sparse Vectors

# %% [markdown]
# To create the sparse vectors we'll use BM25. We import the BM25 function from the [`pinecone-text` library](https://github.com/pinecone-io/pinecone-text).

# %%
from pinecone_text.sparse import BM25Encoder

bm25 = BM25Encoder()

# %% [markdown]
# The tokenization will look something like this:

# %%
"Turtle Check Men Navy Blue Shirt".lower().split()

# %% [markdown]
# BM25 requires training on a representative portion of the dataset. We do this like so:

# %%
bm25.fit(metadata['productDisplayName'])

# %% [markdown]
# Let's create a test sparse vector using a `productDisplayName`.

# %%
metadata['productDisplayName'][0]

# %%
bm25.encode_queries(metadata['productDisplayName'][0])

# %% [markdown]
# And for the stored docs, we only need the "IDF" part:

# %%
bm25.encode_documents(metadata['productDisplayName'][0])

# %% [markdown]
# ## Dense Vectors

# %% [markdown]
# We will use the CLIP to generate dense vectors for product images. We can directly pass PIL images to CLIP as it can encode both images and texts. We can load CLIP like so:
# 
# ## Images is an array of PIL objects (Dense Vectors are made on it)
# ## Metadata is a pandas datafram object (Sparse Vectors are made on it)
# ## 

# %%
from sentence_transformers import SentenceTransformer
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# load a CLIP model from huggingface
model = SentenceTransformer(
    'sentence-transformers/clip-ViT-B-32',
    device=device
)
model

# %%
dense_vec = model.encode([metadata['productDisplayName'][0]])
dense_vec.shape

# %% [markdown]
# The model gives us a `512` dimensional dense vector.

# %% [markdown]
# ## Upsert Documents

# %% [markdown]
# Now we can go ahead and generate sparse and dense vectors for the full dataset and upsert them along with the metadata to the new hybrid index. We can do that easily as follows:

# %%
from tqdm.auto import tqdm

batch_size = 200

for i in tqdm(range(0, len(data), batch_size)):
    # find end of batch
    i_end = min(i+batch_size, len(data))
    # extract metadata batch
    meta_batch = metadata.iloc[i:i_end]
    meta_dict = meta_batch.to_dict(orient="records")
    # concatinate all metadata field except for id and year to form a single string
    # meta_batch_text = [" ".join(row) for row in meta_batch.values.tolist()]
    meta_batch_text = [" ".join(str(value) for value in row) for row in meta_batch.values.tolist()]
    # extract image batch
    img_batch = images[i:i_end]
    # create sparse BM25 vectors
    sparse_embeds = bm25.encode_documents([text for text in meta_batch])
    # create dense vectors
    dense_embeds = model.encode(img_batch).tolist()
    # create unique IDs
    ids = [str(x) for x in range(i, i_end)]

#     upserts = []
#     # loop through the data and create dictionaries for uploading documents to pinecone index
#     for _id, sparse, dense, meta in zip(ids, sparse_embeds, dense_embeds, meta_dict):
#         upserts.append({
#             'id': _id,
#             'sparse_values': sparse,
#             'values': dense,
#             'metadata': meta
#         })
#     # upload the documents to the new hybrid index
#     index.upsert(upserts)

# # show index description after uploading the documents
# index.describe_index_stats()

# Error I am getting is AttributeError: 'int' object has no attribute 'describe_index_stats' 
# which could mean is that the index we are having does not have int object into which we can upsert to 


# %% [markdown]
# Following is the upserting done via multithreading
# 

# %%
# from concurrent.futures import ThreadPoolExecutor
# from tqdm.auto import tqdm

# batch_size = 200

# def process_batch(start_idx, end_idx):
#     meta_batch = metadata.iloc[start_idx:end_idx]
#     meta_dict = meta_batch.to_dict(orient="records")
#     # meta_batch_text = [" ".join(x) for x in meta_batch.loc[:, ~meta_batch.columns.isin(['id', 'year'])].values.tolist()]
#     meta_batch_text = [" ".join(str(value) for value in row) for row in meta_batch.values.tolist()]
#     img_batch = images[start_idx:end_idx]
    
#     sparse_embeds = bm25.encode_documents(meta_batch_text)
#     dense_embeds = model.encode(img_batch).tolist()
    
#     ids = [str(x) for x in range(start_idx, end_idx)]
    
#     upserts = []
#     for _id, sparse, dense, meta in zip(ids, sparse_embeds, dense_embeds, meta_dict):
#         upserts.append({
#             'id': _id,
#             'sparse_values': sparse,
#             'values': dense,
#             'metadata': meta
#         })
#     index.upsert(upserts)

# total_records = len(data)

# with ThreadPoolExecutor() as executor:
#     futures = []
#     for i in tqdm(range(0, total_records, batch_size)):
#         i_end = min(i + batch_size, total_records)
#         future = executor.submit(process_batch, i, i_end)
#         futures.append(future)
    
#     # Wait for all futures to complete
#     for future in futures:
#         future.result()

# index.describe_index_stats()


# %% [markdown]
# 

# %% [markdown]
# ## Querying

# %% [markdown]
# Now we can query the index, providing the sparse and dense vectors. We do this directly with an equal weighting between sparse and dense like so:

# %%
query = "dark blue french connection jeans for men"

# create sparse and dense vectors
sparse = bm25.encode_queries(query)
dense = model.encode(query).tolist()
# search
result = index.query(
    top_k=14,
    vector=dense,
    sparse_vector=sparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
imgs

# %% [markdown]
# We return a list of PIL image objects, to view them we will define a function called `display_result`.

# %%
from IPython.core.display import HTML
from io import BytesIO
from base64 import b64encode

# function to display product images
def display_result(image_batch):
    figures = []
    for img in image_batch:
        b = BytesIO()  
        img.save(b, format='png')
        figures.append(f'''
            <figure style="margin: 5px !important;">
              <img src="data:image/png;base64,{b64encode(b.getvalue()).decode('utf-8')}" style="width: 90px; height: 120px" >
            </figure>
        ''')
    return HTML(data=f'''
        <div style="display: flex; flex-flow: row wrap; text-align: center;">
        {''.join(figures)}
        </div>
    ''')

# %% [markdown]
# And now we can view them:

# %%
display_result(imgs)

# %% [markdown]
# It's possible to prioritize our search based on sparse vs. dense vector results. To do so, we scale the vectors, for this we'll use a function named `hybrid_scale`.

# %%
def hybrid_scale(dense, sparse, alpha: float):
    """Hybrid vector scaling using a convex combination

    alpha * dense + (1 - alpha) * sparse

    Args:
        dense: Array of floats representing
        sparse: a dict of `indices` and `values`
        alpha: float between 0 and 1 where 0 == sparse only
               and 1 == dense only
    """
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    # scale sparse and dense vectors to create hybrid search vecs
    hsparse = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse

# %% [markdown]
# First, we will do a pure sparse vector search by setting the alpha value as 0.

# %%
question = "dark blue french connection jeans for men"

# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# Let's take a look at the description of the result.

# %%
for x in result["matches"]:
    print(x["metadata"]['productDisplayName'])

# %% [markdown]
# We can observe that the keyword search returned French Connection jeans but failed to rank the men's French Connection jeans higher than a few of the women's. Now let's do a pure semantic image search by setting the alpha value to 1.

# %%
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=1)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %%
for x in result["matches"]:
    print(x["metadata"]['productDisplayName'])

# %% [markdown]
# The semantic image search correctly returned blue jeans for men, but mostly failed to match the exact brand we are looking for — French Connection. Now let's set the alpha value to `0.05` to try a hybrid search that is slightly more dense than sparse search.

# %%
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.05)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %%
for x in result["matches"]:
    print(x["metadata"]['productDisplayName'])

# %% [markdown]
# By performing a mostly sparse search with some help from our image-based dense vectors, we get a strong number of French Connection jeans, that are for men, and visually are almost all aligned to blue jeans.

# %% [markdown]
# Let's try more queries.

# %%
query = "small beige handbag for women"
# create sparse and dense vectors
sparse = bm25.encode_queries(query)
dense = model.encode(query).tolist()
# scale sparse and dense vectors - keyword search first
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# We get a lot of small handbags for women, but they're not beige. Let's use the image dense vectors to weigh the colors higher.

# %%
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.05)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %%
for x in result["matches"]:
    print(x["metadata"]['productDisplayName'])

# %% [markdown]
# Here we see better aligned handbags.

# %%
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=1)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# If we go too far with dense vectors, we start to see a few purses, rather than handbags.

# %% [markdown]
# Let's run some more interesting queries. This time we will use a **product image** to create our dense vector, we'll provide a text query as before that will be used to create the sparse vector, and then we'll select a specific color as per the metadata attached to each image, with [metadata filtering](https://docs.pinecone.io/docs/metadata-filtering).

# %%
images[36254]

# %%
query = "soft purple topwear"
# create the sparse vector
sparse = bm25.encode_queries(query)
# now create the dense vector using the image
dense = model.encode(images[36254]).tolist()
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.3)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True
)
# use returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# Our "purple" component isn't being considered strongly enough, let's add this to the metadata filtering:

# %%
query = "soft purple topwear"
# create the sparse vector
sparse = bm25.encode_queries(query)
# now create the dense vector using the image
dense = model.encode(images[36254]).tolist()
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.3)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True,
    filter={"baseColour": "Purple"}  # add to metadata filter
)
# used returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# Let's try with another image:

# %%
images[36256]

# %%
query = "soft green color topwear"
# create the sparse vector
sparse = bm25.encode_queries(query)
# now create the dense vector using the image
dense = model.encode(images[36256]).tolist()
# scale sparse and dense vectors
hdense, hsparse = hybrid_scale(dense, sparse, alpha=0.6)
# search
result = index.query(
    top_k=14,
    vector=hdense,
    sparse_vector=hsparse,
    include_metadata=True,
    filter={"baseColour": "Green"}  # add to metadata filter
)
# use returned product ids to get images
imgs = [images[int(r["id"])] for r in result["matches"]]
# display the images
display_result(imgs)

# %% [markdown]
# Here we did not specify the gender but the search results are accurate and we got products matching our query image and description.

# %% [markdown]
# # Delete the Index
# 
# If you're done with the index, we delete it to save resources.

# %%
pinecone.delete_index(index_name)

# %% [markdown]
# ---


