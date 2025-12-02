import pandas as pd
import streamlit as st
import time
from app.services.upload_service import *


# Set page config first
st.set_page_config(
    page_title="Data Analysis Platform",
    layout="wide"
)

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access this page.")
    st.stop()

# Welcome message with better styling
placeholder = st.empty()
with placeholder.container():
    st.success(f"Welcome back, {st.session_state['username']}!")

time.sleep(2)
placeholder.empty()

# Main content
st.title("Data Analysis Platform")
st.markdown("---")

# Header section
col_header1, col_header2 = st.columns([2, 1])

with col_header1:
    st.header("Select Your Analysis Domain")
    st.markdown("Choose from the available domains below to begin your data analysis.")

with col_header2:
    st.info("Use the sidebar to upload and preview your data files.")

st.markdown("---")

# Domain selection cards
st.subheader("Available Domains")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Cyber Security")
    st.markdown("Analyze security incidents, threats, and vulnerability data.")
    if st.button("Select Cyber Security", key="cyber_btn", use_container_width=True):
        st.session_state.page = "cyber"
        st.switch_page("pages/2_cyber_incidents.py")
    st.image("images/cyber.jpeg", use_container_width=True)

with col2:
    st.markdown("### Datasets Metadata")
    st.markdown("Manage and analyze dataset information and metadata.")
    if st.button("Select Datasets Metadata", key="metadata_btn", use_container_width=True):
        st.session_state.page = "users"
        st.switch_page("pages/3_datasets metadata.py")
    st.image("images/cyber.jpeg", use_container_width=True)

with col3:
    st.markdown("### IT Tickets")
    st.markdown("Process and analyze IT support ticket data.")
    if st.button("Select IT Tickets", key="tickets_btn", use_container_width=True):
        st.session_state.page = "tickets"
        st.switch_page("pages/4_It tickets.py")
    st.image("images/cyber.jpeg", use_container_width=True)

st.markdown("---")

# Sidebar upload section
st.sidebar.title("File Management")
st.sidebar.markdown("---")

upload_on = st.sidebar.toggle("Enable File Upload", value=False)

if upload_on:
    st.sidebar.subheader("Upload CSV File")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file for analysis"
    )

    if uploaded_file is not None:
        try:
            # Read CSV safely
            df = pd.read_csv(uploaded_file, encoding='utf-8')

            # File info in sidebar
            st.sidebar.success("File uploaded successfully!")
            st.sidebar.metric("Rows", len(df))
            st.sidebar.metric("Columns", len(df.columns))

            # Display file contents in main area
            st.subheader("Uploaded File Preview")
            st.dataframe(df, use_container_width=True)

            #
            #  CATEGORY + STATUS BAR CHARTS SIDE BY SIDE
            #
            st.subheader("Category & Status Charts")

            col1, col2 = st.columns(2)

            with col1:
                if "category" in df.columns:
                    st.markdown("### Category")
                    st.bar_chart(df["category"].value_counts())
                else:
                    st.info("No 'category' column found.")

            with col2:
                if "status" in df.columns:
                    st.markdown("### Status")
                    st.bar_chart(df["status"].value_counts())
                else:
                    st.info("No 'status' column found.")

            st.markdown("---")

            #
            #  AUTO-GENERATED BAR CHARTS FOR ALL OTHER COLUMNS
            #
            st.subheader("Other Columns")

            # Detect column types
            categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

            # ---- CATEGORICAL COLUMNS ----
            if len(categorical_cols) > 0:
                st.markdown("Categorical Columns")

                for col in categorical_cols:
                    st.markdown(f"**{col}**")
                    counts = df[col].value_counts()
                    st.bar_chart(counts)
                    st.markdown("---")
            else:
                st.info("No categorical columns available for bar charts.")

            # NUMERIC COLUMNS
            if len(numeric_cols) > 0:
                st.markdown("Numerical Columns")

                for col in numeric_cols:
                    st.markdown(f"**{col}**")
                    st.bar_chart(df[col])
                    st.markdown("---")
            else:
                st.info("No numeric columns available for bar charts.")

            #

        except Exception as e:
            st.sidebar.error(f"Error reading file: {e}")
else:
    clear_uploads_table()
    st.sidebar.info("Toggle on to upload and preview files.")
