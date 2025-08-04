import numpy as np
import faiss

# FAISS index example for demonstration purposes
# This code snippet creates a simple FAISS index with random data.


vector_dim = 6                        # vector dimension
data_set_size = 50                     # database size
query_set_size = 5                       # number of queries

np.random.seed(1234)

# Generate random vectors for the database and queries
data_set = np.random.random((data_set_size, vector_dim)).astype('float32')

data_set[:, 0] += np.arange(data_set_size) / 1000.
print(f"dataset.shape: {data_set.shape}")
print(f"{data_set[:10]}")

query_set = np.random.random((query_set_size, vector_dim)).astype('float32')
query_set[:, 0] += np.arange(query_set_size) / 1000.
print(f"query_set.shape: {query_set.shape}")
print(f"{query_set[:10]}")

 # initialize the index
index = faiss.IndexFlatL2(vector_dim)  
print(index.is_trained)

# add vectors to the index
index.add(data_set)
print(index.ntotal)

# find the k nearest neighbors, use data_set as query for a test
kNearest = 5
distances, searchIndex = index.search(data_set[:5], kNearest)
print(searchIndex)
print(distances)

# find the k nearest neighbors, use query_set now
distances, searchIndex = index.search(query_set, kNearest)
print(searchIndex[:5])
print(distances)
