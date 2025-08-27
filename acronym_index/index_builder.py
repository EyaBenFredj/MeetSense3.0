import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # ✅ local model

load_dotenv()

def build_index():
    print("[🔧] Building Acronym Index...")

    # Project root (absolute paths)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "mock_data")
    persist_path = os.path.join(base_dir, "acronym_index")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"🚫 Folder not found: {data_path}")

    # ✅ Load docs
    documents = SimpleDirectoryReader(input_dir=data_path).load_data()

    # ✅ Use local embedding model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # ✅ Build and persist index
    index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
    index.storage_context.persist(persist_dir=persist_path)

    print(f"[✅] Acronym index saved to: {persist_path}")

if __name__ == "__main__":
    build_index()
