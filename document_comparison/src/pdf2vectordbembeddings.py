import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb

model_name = 'all-MiniLM-L6-v2'


def extract_text_from_pdf(pdf_path, debug=False):

    full_text = ""
    with fitz.open(pdf_path) as doc:
        text= ""
        # 2. Iterate through each page
        for page in doc:
            # 3. Extract text from the page and append it
            text = page.get_text()
            if debug:
                print(f"Page {page.number}: {text[:100]}...")
            full_text += text

    return full_text

    
def chunk_text(full_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_text(full_text)
    return chunks

def main():
    doc1_path = "../assets/4108-2_din_202-12_entwurf.pdf"
    doc2_path = "../assets/4108-2_din_2013_02.pdf"
    full_text = extract_text_from_pdf(doc1_path)

    print(f"Document 1 Text: {full_text[10000:14000]}...")

    chunks1 = chunk_text(full_text)
    full_text = extract_text_from_pdf(doc2_path)
    chunks2 = chunk_text(full_text)

    print(f"Chunks from {doc1_path}: {len(chunks1)}")
    print(f"Chunks from {doc2_path}: {len(chunks2)}")

    model = SentenceTransformer(model_name)

    doc_a_embeddings = model.encode(chunks1)
    doc_b_embeddings = model.encode(chunks2)

    # It's good practice to convert the embeddings to a list of lists
    doc_a_embeddings_list = doc_a_embeddings.tolist()
    doc_b_embeddings_list = doc_b_embeddings.tolist()

    print(f"Successfully generated {len(doc_a_embeddings_list)} embeddings.")
    print(f"Successfully generated {len(doc_b_embeddings_list)} embeddings.")


    print(f"doc_a has stored {doc_a_embeddings.shape[0]} chunks with {doc_a_embeddings.shape[1]} dimensions each.")
    print(f"It's shape is therefore: {doc_a_embeddings.shape}")
    print(f"The vector dimensions were created from the model used: {model_name}")

    print(f"doc_b has stored {doc_b_embeddings.shape[0]} chunks with {doc_b_embeddings.shape[1]} dimensions each.")
    print(f"It's shape is therefore: {doc_b_embeddings.shape}")
    print(f"The vector dimensions were created from the model used: {model_name}")

    # set up a chromadb collection to search for matches between Document A and Document B
    # default embedding model is 'all-MiniLM-L6-v2'
    client = chromadb.Client()
    collection = client.create_collection(name="din_4108")

#    collection.add(
#    ids=["id1", "id2", "id3", ...],
#    documents=chunks1,
#        # metadatas=[{"chapter": 3, "verse": 16}, {"chapter": 3, "verse": 5}, {"chapter": 29, "verse": 11}, ...],
#    )

    # Add Document A embeddings to the collection
    for i, embedding in enumerate(doc_b_embeddings):
        collection.add(ids=f"B_{i}", embeddings=[embedding])

    # Add Document B embeddings to the collection
#    for i, embedding in enumerate(doc_b_embeddings):
#        collection.add(embedding, metadata={"chunk_index": i, "document": "B"})

    kNearest = 3
    print(f"Searching for {kNearest} nearest neighbors in Document B")
    results = collection.query(doc_a_embeddings, n_results=kNearest)

    print(f"Matched indices in Document B:")
    print(f"{results['ids']}")

    print(f"Distances:")
    print(f"{results['distances']}")

    # Keep track of which Doc B chunks have been matched
    # matched_b_chunks = set(matched_indices.flatten())

    # Find all matched chunks in Document B

if __name__ == "__main__":
    main()
