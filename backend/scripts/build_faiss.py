import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ✅ Load SentenceTransformer model
print("🔁 Loading SentenceTransformer model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✅ Model loaded successfully!")

# ✅ Dynamically determine paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
questions_path = os.path.join(BASE_DIR, "..", "data", "police_faqs.json")
faiss_index_path = os.path.join(BASE_DIR, "..", "models", "faiss_index", "police_faqs.index")

# ✅ Load questions and answers from JSON
print(f"🔁 Loading questions from: {questions_path}")
with open(questions_path, "r", encoding="utf-8") as f:
    qa_data = json.load(f)

# ✅ Extract questions for embedding
questions = [item["question"] for item in qa_data]
if not questions:
    raise ValueError("⚠️ No questions found in the JSON file. Check the file content!")

print(f"✅ {len(questions)} questions loaded successfully!")

# ✅ Generate embeddings for questions
print("🔁 Generating embeddings...")
question_embeddings = model.encode(questions)

# ✅ Create and initialize FAISS index
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
print(f"✅ FAISS index initialized with dimension: {dimension}")

# ✅ Add question embeddings to the index
index.add(np.array(question_embeddings))
print(f"✅ {len(questions)} embeddings added to the FAISS index.")

# ✅ Save FAISS index to file
faiss.write_index(index, faiss_index_path)
print(f"✅ FAISS index saved to: {faiss_index_path}")


# ✅ Optional: Function to rebuild FAISS index from app.py
def rebuild_faiss_index():
    print("🔁 Rebuilding FAISS index...")
    question_embeddings = model.encode(questions)
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(question_embeddings))
    faiss.write_index(index, faiss_index_path)
    print(f"✅ FAISS index rebuilt successfully with {len(questions)} entries!")
