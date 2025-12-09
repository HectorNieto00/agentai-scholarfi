import streamlit as st
import re
from pathlib import Path
from utils.styles import register_css
from database.db_methods import create_user, get_user_by_email

def is_strong_password(password):
        # Al menos 8 caracteres, 1 dígito, 1 letra, 1 caracter especial
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&^_-])[A-Za-z\d@$!#%*?&^_-]{8,}$'
        return re.match(pattern, password)

def run():
    # --- Load CSS ---
    register_css()

    st.markdown('<h1 style="font-size: 2.5em; font-weight: bold; color: #4a73ff">Create Account</h1>', unsafe_allow_html=True)

    name = st.text_input("Name", key="reg_name")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")

    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    if st.button("Register"):
        if not name or not email or not password:
            st.warning("Please fill in all fields.")
        elif not is_valid_email(email):
            st.warning("Please enter a valid email address.")
        elif not is_strong_password(password):
            st.warning("Password must be at least 8 characters long and include at least 1 letter, 1 number, and 1 special character.")
        elif password != confirm_password:
            st.error("Passwords do not match!")
        else:
            # Verificar si el email ya existe en la DB
            existing_user = get_user_by_email(email)
            if existing_user:
                st.error("User with this email already exists.")
            else:
                # Crear usuario en la DB
                user_id = create_user(name=name, email=email, password=password)
                if user_id:
                    st.success(f"User {name} registered successfully!")
                    st.session_state.page = "login"
                else:
                    st.error("Error creating user. Please try again.")

    if st.button("Go to Login"):
        st.session_state.page = "login"
