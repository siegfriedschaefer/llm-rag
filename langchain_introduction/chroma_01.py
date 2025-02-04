import chromadb

# Import the embedding function you want to use.
# is needed because of my Intel Mac.
from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2


client = chromadb.Client()

# create an embedded function variable 
ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])

# finally, modiy your `get_or_create_collection` statement by passing the embedding_function parameter
collection = client.get_or_create_collection("collection_01", metadata={"hnsw:space": "cosine"}, embedding_function=ef)

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
collection.add(
    documents=["This is document1", "This is document2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
    metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
    ids=["doc1", "doc2"], # unique for each doc
)

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)

print(results)

