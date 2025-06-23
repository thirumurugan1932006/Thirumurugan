import sqlite3
import streamlit as st
import bcrypt

# Database connection
def connect_db():
    return sqlite3.connect("database/chatbot.db")

# Create tables if not exists
def setup_db():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY, username TEXT, password TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY, user TEXT, query TEXT, response TEXT, timestamp TEXT)""")
    conn.commit()
    conn.close()

# Signup Page
def signup_page():
    st.subheader("Signup")
    uname = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Signup"):
        conn = connect_db()
        c = conn.cursor()
        hashed = bcrypt.hashpw(passwd.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (uname, hashed))
        conn.commit()
        st.success("Account created! Please login.")
        conn.close()

# Login Page
def login_page():
    st.subheader("Login")
    uname = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Login"):
        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (uname,))
        result = c.fetchone()
        if result and bcrypt.checkpw(passwd.encode(), result[0]):
            st.session_state.logged_in = True
            st.session_state.username = uname
            st.success(f"Welcome, {uname}!")
        else:
            st.error("Invalid login.")
        conn.close()

# Profile Page
def profile_page():
    st.subheader("Profile (Coming soon)")

# Chat History
def history_page():
    st.subheader("Chat History")
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT query, response, timestamp FROM chat_history WHERE user=?", (st.session_state.username,))
    history = c.fetchall()
    for q, r, t in history:
        st.write(f"**{t}**")
        st.write(f"**You:** {q}")
        st.write(f"**Bot:** {r}")
        st.markdown("---")
    conn.close()
  
