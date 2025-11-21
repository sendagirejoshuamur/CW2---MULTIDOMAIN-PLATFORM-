import streamlit as st

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access this page.")
    st.stop()


st.title("Welcome to the Home Page! 🏠")
st.success("You have successfully registered and logged in!")

# Add your home page content here
st.write("This is your home page after successful registration.")