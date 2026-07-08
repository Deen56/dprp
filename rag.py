import os
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from questions import QUESTIONS

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load and chunk the knowledge base
def load_knowledge_base():
    with open("knowledge.txt", "r") as f:
        content = f.read()
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    return chunks

# Convert all chunks to vectors
def embed_chunks(chunks):
    chunk_vectors = []
    for chunk in chunks:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents=chunk
        )
        vector = result.embeddings[0].values
        chunk_vectors.append(vector)
    return chunk_vectors

# Find the most relevant chunk for a question
def get_relevant_chunk(question, chunks, chunk_vectors):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question
    )
    question_vector = np.array(result.embeddings[0].values)

    best_score = -1
    best_chunk = ""

    for i, chunk_vector in enumerate(chunk_vectors):
        chunk_vec = np.array(chunk_vector)
        score = np.dot(question_vector, chunk_vec) / (
            np.linalg.norm(question_vector) * np.linalg.norm(chunk_vec)
        )
        if score > best_score:
            best_score = score
            best_chunk = chunks[i]

    return best_chunk

# Generate a response using the relevant chunk
def ask_veyr(question, chat, chunks, chunk_vectors, user_id=None):
    relevant_chunk = get_relevant_chunk(question, chunks, chunk_vectors)
    
    # Build context with tools if user_id is available
    tool_context = ""
    if user_id:
        score_info = get_user_latest_score(user_id)
        weak_areas = get_user_weak_areas(user_id)
        tool_context = f"""
User's actual data:
{score_info}
{weak_areas}
"""

    prompt = f"""Context from knowledge base: {relevant_chunk}

{tool_context}

Question: {question}

Answer based on the context and user data above. Be specific and personalised if user data is available."""

    response = chat.send_message(prompt)
    return response.text

# Initialise everything on startup
chunks = load_knowledge_base()
chunk_vectors = embed_chunks(chunks)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are Veyr, a friendly and helpful assistant for the Digital Privacy Risk Assessment Platform (DPRP). Help users understand their privacy risk scores and how to improve their digital privacy. Answer only based on the context provided."
    )
)

def get_user_latest_score(user_id):
    from models import Assessment
    assessment = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.taken_at.desc()).first()
    if not assessment:
        return "No assessment found for this user."
    return f"Latest score: {assessment.score}, Risk level: {assessment.risk_level}, Date: {assessment.taken_at.strftime('%Y-%m-%d')}"

def get_user_weak_areas(user_id):
    from models import Assessment, Answer
    assessment = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.taken_at.desc()).first()
    if not assessment:
        return "No assessment found."
    
    answers = Answer.query.filter_by(assessment_id=assessment.id).all()
    
    weak_areas = []
    for answer in answers:
        if answer.answer_value == 1:
            for question in QUESTIONS:
                if question['id'] == answer.question_id:
                    weak_areas.append(f"{question['category']}: {question['text']}")
    
    if not weak_areas:
        return "No weak areas found — great privacy practices!"
    
    return "Weak areas:\n" + "\n".join(weak_areas)
