import numpy as np

# FAISS index example for demonstration purposes
# This code snippet creates a simple FAISS index with random data.


d = 6                        # dimension
nb = 50                      # database size
nq = 5                       # number of queries

np.random.seed(1234)
xb = np.random.random((nb, d)).astype('float32')

xb[:, 0] += np.arange(nb) / 1000.
print(f"xb.shape: {xb.shape}")
print(f"{xb[:10]}")

xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.
print(f"xq.shape: {xq.shape}")
print(f"{xq[:10]}")
