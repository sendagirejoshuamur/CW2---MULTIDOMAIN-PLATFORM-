import streamlit as st
from pathlib import Path
from app.services.user_service import *
import auth
import time
import os

conn = connect_database()

# ---------------------- SESSION STATE ----------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# ---------------------- STYLING ----------------------
st.set_page_config(page_title="SJ's MultiDomain Platform", layout="centered")
st.markdown("---")

st.title("WELCOME TO SJ's MULTIDOMAIN PLATFORM ")
st.markdown("---")

# ---------------------- SHOW LOGIN/REGISTER ONLY IF NOT LOGGED IN ----------------------
if not st.session_state["logged_in"]:
    st.subheader("Please choose an option below:")
    choice = st.selectbox("Select Action", ["Tap to pick an option", "login", "register"])

    # Registration validators
    continue_reg_username = 0
    continue_reg_password = 0
    continue_reg_password_confirmation = 0
    continue_reg_exists = 0
    continue_login_username_and_password = 0

    # ---------------------- REGISTRATION ----------------------
    if choice == "register":
        st.markdown("Create Your Account")
        username = st.text_input("Username").strip()

        is_valid, error_msg = auth.validate_username(username)
        if username and not is_valid:
            st.error(error_msg)
        else:
            continue_reg_username = 1

        if username and auth.user_exists(username):
            st.error("Username already exists! Please choose a different username.")
        else:
            continue_reg_exists = 1

        password = st.text_input("Password", type="password").strip()

        # PASSWORD STRENGTH METER
        if password:
            strength = 0
            feedback = []

            if len(password) >= 8: strength += 1
            else: feedback.append("At least 8 characters")
            if any(c.isupper() for c in password) and any(c.islower() for c in password): strength += 1
            else: feedback.append("Mix of uppercase and lowercase")
            if any(c.isdigit() for c in password): strength += 1
            else: feedback.append("At least one number")
            if any(not c.isalnum() for c in password): strength += 1
            else: feedback.append("At least one special character")

            strength_labels = ["Weak", "Weak", "Fair", "Good", "Strong"]
            comment = ["Come on bro", "P___y", "Okay", "That's alright", "That's my boy"]

            col1, col2 = st.columns([1,4])
            with col1:
                st.metric("Strength", strength_labels[strength])
            with col2:
                st.progress(strength / 4)
                st.caption(f"Password feedback: {comment[strength].title()}")

            if strength < 4 and feedback:
                with st.expander("Tips to improve your password"):
                    for tip in feedback:
                        st.write(f"• {tip}")

        is_valid, error_msg = auth.validate_password(password)
        if password and not is_valid:
            st.error(error_msg)
        else:
            continue_reg_password = 1

        password_confirmation = st.text_input("Confirm Password", type="password")
        if password and password != password_confirmation:
            st.error("Passwords do not match")
        else:
            continue_reg_password_confirmation = 1

        role = st.selectbox("Select your role", ["pick an option", "admin", "user"])
        agree = st.checkbox("I agree to give Joshua Sendagire a first class after viewing this dashboard")

    # ---------------------- LOGIN ----------------------
    elif choice == "login":
        st.markdown("### Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if username == "": st.warning("Please enter your username")
        if password == "": st.warning("Please enter your password")

    # ---------------------- PROCEED BUTTON ----------------------
    if st.button("Proceed"):
        # Registration submit
        if choice == "register":
            if (continue_reg_username == 1 and
                continue_reg_password == 1 and
                continue_reg_password_confirmation == 1 and
                continue_reg_exists == 1 and
                role != "pick an option" and
                agree):

                auth.register_user(username, password, role)
                with st.spinner('Loading data...'):
                    time.sleep(2)
                st.success('Registration successful!')
                st.balloons()
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                migrate_users_from_file()
                st.switch_page("pages/1_Home.py")
            else:
                st.warning("Failed to register. Please check your inputs!")

        # Login submit
        elif choice == "login":
            login_result = auth.login_user(username, password)
            if login_result:
                with st.spinner('Logging in...'):
                    time.sleep(2)
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["is_admin"] = login_result == "admin"
                st.success('Logged in successfully!')
                time.sleep(1)
                st.switch_page("pages/1_Home.py")
            else:
                st.error("Invalid username or password")

# ---------------------- WHEN LOGGED IN ----------------------
else:
    st.markdown(f"You are logged in as {st.session_state['username']}")
    if st.session_state["is_admin"]:
        st.success("ADMIN ACCESS GRANTED")
    if st.button("Log out"):
        with st.spinner('Logging out...'):
            time.sleep(1)
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["is_admin"] = False
        st.rerun()

conn.close()
