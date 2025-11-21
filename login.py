import streamlit as st
from pathlib import Path
import auth
import time
import os

# creating and intializing session state variables
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

# ---------------------- SHOW LOGIN/REGISTER ONLY IF NOT LOGGED IN ----------------------
if not st.session_state["logged_in"]:

    # sj needs a first class -----PAGE BEGINS FROM HERE -------sj needs a first class

    st.title("WELCOME TO SJ's MULTIDOMAIN PLATFORM")

    st.header("Would you like to login or register?")
    choice = st.selectbox("Please pick an option", ["Tap to pick an option", "login", "register"])

    # Registration validators
    continue_reg_username = 0
    continue_reg_password = 0
    continue_reg_password_confirmation = 0
    continue_reg_exists = 0

    continue_login_username_and_password = 0

    # sj needs a first class -----REGISTRATION SECTION -------sj needs a first class

    if choice == "register":
        username = st.text_input("Enter your username:")
        username.strip()

        is_valid, error_msg = auth.validate_username(username)
        if not is_valid:
            st.write(f":red[{error_msg}]")
        else:
            continue_reg_username = 1

        if auth.user_exists(username):
            st.markdown(":red[Username exists! Please choose a different username.]")
        else:
            continue_reg_exists = 1

        password = st.text_input("Enter your password:", type="password")
        password.strip()
        is_valid, error_msg = auth.validate_password(password)
        if not is_valid:
            st.markdown(f":red[{error_msg}]")
        else:
            continue_reg_password = 1

        password_confirmation = st.text_input("Enter your password again:", type="password")
        if password != password_confirmation:
            st.markdown(":red[Passwords do not match]")
        else:
            continue_reg_password_confirmation = 1

        role = st.selectbox("Select your role", ["pick an option", "admin", "user"])
        agree = st.checkbox("I agree to give Joshua Sendagire a first class after viewing this dashboard 😉")

    # sj needs a first class -----LOGIN SECTION -------sj needs a first class

    elif choice == "login":
        username = st.text_input("Enter your username:")
        password = st.text_input("Enter your password:", type="password")
        if username == "":
            st.warning(":red[Please enter your username]")
        if password == "":
            st.warning(":red[Please enter your password]")
        if auth.login_user(username, password):
            with st.spinner('Loading data... Please wait!'):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
        else:
            st.error("Invalid username or password")

    # PROCEED BUTTON CONTROL
    if st.button("proceed"):

        # REGISTRATION SECTION
        if choice == "register":
            if (continue_reg_username == 1 and
                continue_reg_password == 1 and
                continue_reg_password_confirmation == 1 and
                continue_reg_exists == 1):

                auth.register_user(username, password)
                # simulating a spinner for 3 seconds
                with st.spinner('Loading data... Please wait!'):
                    time.sleep(3)
                st.success('registration successfully!')
                st.balloons()

                # assigning session state true and username so that the user stays logged in
                st.session_state["logged_in"] = True
                st.session_state["username"] = username

                st.switch_page("pages/home.py")
            else:
                st.warning(":red[Failed to register user! Please check your username and password]")

        # LOGIN SECTION
        elif choice == "login":
            if continue_login_username_and_password == 1:
                time.sleep(3)
                st.success('logged in successfully!')
                time.sleep(1)
                continue_login_username_and_password = 1
                st.switch_page("pages/home.py")
            else:
                st.warning(":red[Failed to login user! Please check your username and password]")



# sj needs a first class -----THIS WILL SHOW ONLY WHEN SOME ONE IS LOGGED IN -------sj needs a first class
else:
    st.title("You are logged in!")
    st.write(f"Logged in as **{st.session_state['username']}**")

    if st.button("Log out"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()
