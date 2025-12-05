import streamlit as st
from pages_public import LogIn, Register
from pages_private import Dashboard, Finance_Hub
from database.database import init_db
from utils.auth import logout

# --- Initialize DB ---
init_db()

# --- Initialize session state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"

# --- NAVIGATION ---
if st.session_state.logged_in:
    # Mostrar sidebar solo si está logueado
    st.sidebar.title(f"Hello, {st.session_state.user_name}")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Finance Hub"])
    if st.sidebar.button("Logout"):
        logout()
        st.session_state.page = "login"

    if page == "Dashboard":
        Dashboard.run()
    elif page == "Finance Hub":
        Finance_Hub.run()
else:
    # Páginas públicas
    if st.session_state.page == "login":
        LogIn.run()
    elif st.session_state.page == "register":
        Register.run()