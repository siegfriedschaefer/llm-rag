# importing required modules
from pypdf import PdfReader
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


def extract_text_from_pdf(pdf_path):

    full_text = ""
    with fitz.open(pdf_path) as doc:
        i=0
        text= ""
        # 2. Iterate through each page
        for page in doc:
            # 3. Extract text from the page and append it
            text = page.get_text()
            if text and i == 3:
                print("==========================")
                print(text)
                print("==========================")
            i += 1
            full_text += text

#    reader = PdfReader(pdf_path)

#    i=0
#    for page in reader.pages:
#        # printing the text of each page
#        text = page.extract_text()
#        if text and i == 3:
#            print("==========================")
#            print(text)
#            print("==========================")
#        i+=1

    # extracting text from each page and joining them
#    full_text = "".join(page.extract_text() for page in reader.pages)

    return full_text

    
def chunk_text(full_text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
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

    model = SentenceTransformer('all-MiniLM-L6-v2')

    doc_a_embeddings = model.encode(chunks1)
    doc_b_embeddings = model.encode(chunks2)

    similarities = model.similarity(doc_a_embeddings, doc_b_embeddings)

    print(f"Similarities.len: {len(similarities)} ")

    print(f"doc_a_embeddings.shape: {doc_a_embeddings.shape}")
    print(f"doc_b_embeddings.shape: {doc_b_embeddings.shape}")

    # Build the FAISS index for Document B
    index = faiss.IndexFlatL2(doc_b_embeddings.shape[1])
    index.add(np.array(doc_b_embeddings, dtype=np.float32))

    print(f"Index size: {index.ntotal}")

    print(f"Index: {index.is_trained}")

    # Search for matches for each chunk of Document A
    # D are the distances (lower is better), I are the indices

    ndistances, matched_indices_in_b = index.search(np.array(doc_a_embeddings[93:94], dtype=np.float32), 1)

    print(f"Matched indices in Document B: {matched_indices_in_b}:{ndistances}") 

    # Keep track of which Doc B chunks have been matched
    matched_b_chunks = set(matched_indices_in_b.flatten())

    # Find all matched chunks in Document B
    print(f"{chunks1[93:94]}")
    print("----------------------")
    print(f"{chunks2[80]}")
    print(f"Matched chunks in Document B: {len(matched_b_chunks)}")

if __name__ == "__main__":
    main()
