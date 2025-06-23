import streamlit as st
import spacy
from sentence_transformers import SentenceTransformer
import datetime
import db_manager

# Load NLP and embedding model
nlp = spacy.load("en_core_web_sm")
embed_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Chat Page
def chat_page():
    st.subheader("Chat with Tamil Story Bot")
    user_input = st.text_input("Your query")
    if st.button("Send"):
        chunks = chunk_text(user_input)
        vectors = vectorize_chunks(chunks)
        response = generate_response(user_input, vectors)
        st.success(response)
        save_chat(user_input, response)

# Text Chunking
def chunk_text(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]

# Vectorizing
def vectorize_chunks(chunks):
    return embed_model.encode(chunks)

# Simple Response (replace with LLM integration)
def generate_response(query, vectors):
    return "Once upon a time in Tamil Nadu, there was a king..."

# Save Chat to History
def save_chat(query, response):
    conn = db_manager.connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user, query, response, timestamp) VALUES (?, ?, ?, ?)",
              (st.session_state.username, query, response, datetime.datetime.now()))
    conn.commit()
    conn.close()
  
