import os
import re
from chroma_client import get_sop_collection

# Get the ChromaDB collection instance
collection = get_sop_collection()

def extract_text_chunks(txt_path):
    abs_path = os.path.abspath(txt_path)
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    if not content:
        return []

    # Split by paragraph separators
    paragraphs = re.split(r'\n\s*\n', content)
    chunks = []
    for i, para in enumerate(paragraphs):
        text = para.strip()
        if text:
            chunks.append({
                "content": text,
                "metadata": {
                    "source": abs_path,
                    "chunk": i + 1,
                    "filename": os.path.basename(txt_path)
                }
            })
    return chunks

def store_chunks(chunks):
    if not chunks:
        print("No chunks to add.")
        return

    source = chunks[0]["metadata"]["source"]
    filename = chunks[0]["metadata"]["filename"]
    
    # Delete existing chunks for this source
    print(f"Deleting old chunks for: {filename}")
    collection.delete(where={"source": source})

    # Prepare batch data
    documents = []
    metadatas = []
    ids = []
    
    for chunk in chunks:
        documents.append(chunk["content"])
        metadatas.append(chunk["metadata"])
        ids.append(f"{filename}_chunk_{chunk['metadata']['chunk']}")

    # Batch upsert
    batch_size = 100
    try:
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            collection.upsert(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            print(f"Added batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        
        print(f"✅ Added {len(documents)} chunks from {filename}")
        print("Total documents:", collection.count())
    except Exception as e:
        print("❌ Error adding to collection:", repr(e))

if __name__ == "__main__":
    text_folder = "text_sop"

    if not os.path.exists(text_folder):
        print(f"Error: Folder '{text_folder}' not found!")
        exit(1)

    txt_files = [f for f in os.listdir(text_folder) 
                if f.lower().endswith(".txt") and os.path.isfile(os.path.join(text_folder, f))]
    
    if not txt_files:
        print(f"No text files found in '{text_folder}'")
        exit(1)

    print(f"Found {len(txt_files)} text files for processing")
    for txt_file in txt_files:
        txt_path = os.path.join(text_folder, txt_file)
        print(f"\nProcessing {txt_file}...")
        chunks = extract_text_chunks(txt_path)
        
        if chunks:
            store_chunks(chunks)
        else:
            print(f"No content found in {txt_file}")
    
    print("\nDatabase setup completed!")
