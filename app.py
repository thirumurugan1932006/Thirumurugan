import streamlit as st
import db_manager
import chatbot_logic
import web_query

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Page navigation
menu = st.sidebar.selectbox("Menu", ["Login", "Signup", "Chat", "History", "Profile", "Logout"])

if menu == "Login":
    db_manager.login_page()

elif menu == "Signup":
    db_manager.signup_page()

elif menu == "Chat":
    if st.session_state.logged_in:
        chatbot_logic.chat_page()
    else:
        st.warning("Please log in to use the chat.")

elif menu == "History":
    if st.session_state.logged_in:
        db_manager.history_page()
    else:
        st.warning("Please log in to view chat history.")

elif menu == "Profile":
    if st.session_state.logged_in:
        db_manager.profile_page()
    else:
        st.warning("Please log in.")

elif menu == "Logout":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("Logged out successfully.")
  
