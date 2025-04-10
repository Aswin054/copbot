from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from flask_cors import CORS
import os

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# ✅ Load SentenceTransformer model
print("🔁 Loading SentenceTransformer model...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print("✅ Model loaded successfully!")

# ✅ Define dynamic file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
faiss_index_path = os.path.join(BASE_DIR, "models", "faiss_index", "police_faqs.index")
questions_path = os.path.join(BASE_DIR, "data", "police_faqs.json")

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
SIMILARITY_THRESHOLD = 1.0

# ✅ Function to get the best match for a query
def get_response(query):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k=1)
    best_match_idx = I[0][0]
    similarity_score = D[0][0]

    print(f"🔎 Best match index: {best_match_idx}, Distance: {similarity_score:.4f}")

    if best_match_idx == -1 or best_match_idx >= len(qa_data) or similarity_score > SIMILARITY_THRESHOLD:
        return "Sorry, I couldn't find an answer to your query. Please contact your nearest police station for assistance."

    return qa_data[best_match_idx]["answer"]

# ✅ Root route to prevent 404 at /
@app.route("/", methods=["GET"])
def home():
    return "👮‍♂️ CopBot backend is running! Use POST /query to ask a question."

# ✅ Health check
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Backend is running successfully!"})

# ✅ Chat endpoint
@app.route("/query", methods=["POST"])
def chatbot():
    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty query. Please provide a valid query."}), 400

    print(f"👮 Received query: {query}")
    response = get_response(query)
    return jsonify({"response": response})

# ✅ Rebuild FAISS index if needed
@app.route("/rebuild_index", methods=["POST"])
def rebuild_index():
    try:
        from build_faiss import rebuild_faiss_index
        rebuild_faiss_index()
        return jsonify({"status": "FAISS index rebuilt successfully!"})
    except Exception as e:
        return jsonify({"error": f"Failed to rebuild index: {str(e)}"}), 500

# ✅ Run server (with dynamic port binding for Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 CopBot backend running on port {port}")
    app.run(debug=True, host="0.0.0.0", port=port)
