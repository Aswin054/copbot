from docx import Document
import json
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# ✅ Load SentenceTransformer model for deduplication
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


# ✅ Function to extract QA pairs from DOCX properly
def extract_qa_from_docx(file_path):
    doc = Document(file_path)
    qa_pairs = []
    question = None
    answer = []

    for para in doc.paragraphs:
        text = para.text.strip()

        # ✅ Detect a question if it starts with "Q" and ends with "?"
        if text.startswith("Q") and "?" in text:
            # ✅ Save previous Q&A if exists
            if question and answer:
                full_answer = " ".join(answer).strip()
                qa_pairs.append({"question": question, "answer": full_answer})
                answer = []  # Reset for next Q&A

            question = text.split(": ", 1)[-1]  # Remove 'Qx:' from the question
        elif question and text:
            # ✅ Add text as part of the answer
            answer.append(text)
        elif question and not text:
            # ✅ Save the previous QA pair when encountering an empty line
            if question and answer:
                full_answer = " ".join(answer).strip()
                qa_pairs.append({"question": question, "answer": full_answer})
                question, answer = None, []

    # ✅ Handle the last Q&A
    if question and answer:
        full_answer = " ".join(answer).strip()
        qa_pairs.append({"question": question, "answer": full_answer})

    return qa_pairs


# ✅ Function to remove duplicate or highly similar questions
def remove_duplicates(qa_pairs, similarity_threshold=0.85):
    questions = [pair["question"] for pair in qa_pairs]
    question_embeddings = model.encode(questions)
    unique_pairs = []
    seen_indices = set()

    for i, pair in enumerate(qa_pairs):
        if i in seen_indices:
            continue
        unique_pairs.append(pair)

        # ✅ Check for similar questions to remove duplicates
        similarities = cosine_similarity([question_embeddings[i]], question_embeddings)[0]
        for j, sim in enumerate(similarities):
            if sim > similarity_threshold and i != j:
                seen_indices.add(j)

    print(f"✅ Removed {len(qa_pairs) - len(unique_pairs)} duplicate/similar questions.")
    return unique_pairs


# ✅ Function to add a default 'no answer' pair for unrecognized queries
def add_default_pair(qa_pairs):
    unrecognized_query = {
        "question": "unknown_query",
        "answer": "Sorry, I couldn't find an answer to your query. Please contact your nearest police station for further assistance."
    }
    qa_pairs.append(unrecognized_query)
    return qa_pairs


if __name__ == "__main__":
    file_path = r"C:\Users\Lenova\Desktop\cop\backend\data\COPBOT DATABASE.docx"

    # ✅ Extract Q&A pairs
    print("📚 Extracting QA pairs...")
    qa_data = extract_qa_from_docx(file_path)
    print(f"✅ Extracted {len(qa_data)} QA pairs successfully!")

    # ✅ Remove duplicates for better accuracy
    print("🧹 Removing duplicate/similar questions...")
    qa_data = remove_duplicates(qa_data)

    # ✅ Add default unrecognized query pair
    print("🤖 Adding default unrecognized query response...")
    qa_data = add_default_pair(qa_data)

    # ✅ Save as JSON
    output_path = r"C:\Users\Lenova\Desktop\cop\backend\models\faiss_index\questions.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(qa_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Data saved to {output_path} with {len(qa_data)} entries!")
