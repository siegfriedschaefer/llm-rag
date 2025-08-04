# importing required modules
from pypdf import PdfReader
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

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

    similarities = model.similarity(doc_a_embeddings, doc_b_embeddings)

    print(f"Similarities.len: {len(similarities)} ")

    print(f"doc_a has stored {doc_a_embeddings.shape[0]} chunks with {doc_a_embeddings.shape[1]} dimensions each.")
    print(f"It's shape is therefore: {doc_a_embeddings.shape}")
    print(f"The vector dimensions were created from the model used: {model_name}")

    print(f"doc_b has stored {doc_b_embeddings.shape[0]} chunks with {doc_b_embeddings.shape[1]} dimensions each.")
    print(f"It's shape is therefore: {doc_b_embeddings.shape}")
    print(f"The vector dimensions were created from the model used: {model_name}")

    # we are now setting up a FAISS index to search for matches between Document A and Document B
    # We will use the L2 distance metric for this example because it is simple and effective for many use cases
    # In practice, you might want to use a more complex index type depending on your needs.
    print("Setting up FAISS index...")

    # L2b distance search uses a brute-force search, which is simple but can be slow for large datasets.

    # Create the FAISS index for Document B embeddings
    index = faiss.IndexFlatL2(doc_b_embeddings.shape[1])
    index.add(np.array(doc_b_embeddings, dtype=np.float32))

    print(f"index.size: {index.ntotal}")

    print(f"index.is_trained {index.is_trained}")

    # Search for matches for each chunk of Document A
    

    kNearest = 3
    print(f"Searching for {kNearest} nearest neighbors in Document B")
    mdistances, mindices = index.search(doc_a_embeddings[0:1], kNearest)

    print(f"Matched indices in Document B:")
    print(f"{mindices}")
    print(f"Distances:")
    print(f"{mdistances}")

    # Keep track of which Doc B chunks have been matched
    # matched_b_chunks = set(matched_indices.flatten())

    # Find all matched chunks in Document B

if __name__ == "__main__":
    main()
