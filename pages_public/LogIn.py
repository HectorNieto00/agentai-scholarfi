import streamlit as st
from utils.auth import login_user
from utils.styles import load_css

def run():
    # --- Load CSS ---
    load_css()
    
    st.title("Welcome to scholarFi")
    st.write("Please login or register to continue.")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            success, name, user_id = login_user(email, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_id = user_id
                st.success(f"Welcome back, {name}!")
                st.session_state.page = "dashboard"
            else:
                st.error("Invalid email or password!")

    if st.button("Go to Register"):
        st.session_state.page = "register"