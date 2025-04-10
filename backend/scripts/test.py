import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# ✅ Load SentenceTransformer model
print("🔁 Loading SentenceTransformer model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✅ Model loaded successfully!")

# ✅ Define dynamic file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faiss_index_path = os.path.join(BASE_DIR, "..", "models", "faiss_index", "police_faqs.index")
questions_path = os.path.join(BASE_DIR, "..", "data", "police_faqs.json")

# ✅ Load FAISS index and questions data
try:
    print(f"🔁 Loading FAISS index from: {faiss_index_path}")
    index = faiss.read_index(faiss_index_path)

    print(f"🔁 Loading questions from: {questions_path}")
    with open(questions_path, "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    if not qa_data:
        raise ValueError("⚠️ No questions found in the JSON file. Check the file content!")

    print(f"✅ Loaded {len(qa_data)} questions successfully!")
except Exception as e:
    print(f"❌ Error loading FAISS index or questions.json: {e}")
    exit(1)

# ✅ Define similarity threshold for unrecognized queries
SIMILARITY_THRESHOLD = 1.0  # L2 distance threshold (adjust based on your dataset)


# ✅ Function to get the best match for a query
def get_response(query):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)  # Search for the best match
    best_match_idx = I[0][0]
    similarity_score = D[0][0]  # ✅ Correct interpretation of distance (L2)

    # ✅ Debug to check similarity score and best match index
    print(f"🔎 Best match index: {best_match_idx}, Distance: {similarity_score:.4f}")

    # ✅ Check if the best match is valid based on distance
    if best_match_idx == -1 or best_match_idx >= len(qa_data) or similarity_score > SIMILARITY_THRESHOLD:
        return "Sorry, I couldn't find an answer to your query. Please contact your nearest police station for assistance."

    # ✅ Return the verified answer
    return qa_data[best_match_idx]["answer"]


# ✅ Function to test multiple queries (for batch testing)
def test_queries(queries):
    for query in queries:
        response = get_response(query)
        print(f"👮 Question: {query}")
        print(f"🤖 Response: {response}\n")


# ✅ Main loop to ask questions in terminal
def interactive_chat():
    print("🚀 CopBot Chat is ready! Ask your question or type 'exit' to quit.\n")
    while True:
        query = input("👮 Ask your question: ")
        if query.lower() == "exit":
            print("👋 Goodbye!")
            break
        response = get_response(query)
        print(f"🤖 Response: {response}\n")


# ✅ Run the interactive chatbot or batch test if needed
if __name__ == "__main__":
    import sys

    # ✅ Check if batch testing mode or interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_queries([
            "What is the women’s helpline number?",
            "How do I file a complaint if my child is missing?",
            "Where do I report a lost wallet?",
            "qwertyuiop",  # Random query to test fallback
            "My friend is missing, how do I report?",  # Test similarity to child missing
            "How to get a passport?",  # Test unrecognized question
        ])
    else:
        # ✅ Start interactive chat mode by default
        interactive_chat()
