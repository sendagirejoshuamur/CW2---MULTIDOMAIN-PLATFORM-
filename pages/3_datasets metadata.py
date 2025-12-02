import streamlit as st
import pandas as pd
from app.data.datasets import *

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access this page.")
    st.stop()

st.set_page_config(page_title="Datasets Metadata", layout="wide")
st.title("WELCOME! TO THE DATASETS METADATA PAGE")

# Get all datasets
datasets = get_all_datasets()

# Convert to DataFrame for easier manipulation
if datasets:
    df = pd.DataFrame(datasets, columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
    df['upload_date'] = pd.to_datetime(df['upload_date'])
else:
    df = pd.DataFrame()

# SIDEBAR FILTERS
st.sidebar.header("Filters")

# Size filter
if not df.empty:
    min_rows, max_rows = df['rows'].min(), df['rows'].max()
    row_range = st.sidebar.slider("Number of Rows", min_rows, max_rows, (min_rows, max_rows))
    df = df[(df['rows'] >= row_range[0]) & (df['rows'] <= row_range[1])]

# User filter
if not df.empty and 'uploaded_by' in df.columns:
    users = ['All'] + list(df['uploaded_by'].unique())
    selected_user = st.sidebar.selectbox("Uploaded By", users)
    if selected_user != 'All':
        df = df[df['uploaded_by'] == selected_user]

# QUICK STATS
st.subheader("Quick Stats")
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Datasets", len(df))

    with col2:
        total_rows = df['rows'].sum()
        st.metric("Total Rows", f"{total_rows:,}")

    with col3:
        avg_rows = df['rows'].mean()
        st.metric("Avg Rows/Dataset", f"{avg_rows:,.0f}")

    with col4:
        large_count = len(df[df['rows'] > 10000])
        st.metric("Large Datasets (>10k)", large_count)

# SIMPLE CHARTS
st.subheader("Charts")
if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.write("Dataset Size Distribution")
        st.bar_chart(df.set_index('name')['rows'])

    with col2:
        st.write("Datasets by User")
        user_counts = df['uploaded_by'].value_counts()
        st.bar_chart(user_counts)

# DATASET RESOURCE ANALYSIS
st.subheader("Resource Consumption Analysis")

if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Size Categories**")
        # Categorize by size
        small = len(df[df['rows'] <= 1000])
        medium = len(df[df['rows'].between(1001, 10000)])
        large = len(df[df['rows'] > 10000])

        size_data = pd.DataFrame({
            'Category': ['Small (≤1k)', 'Medium (1k-10k)', 'Large (>10k)'],
            'Count': [small, medium, large]
        })
        st.bar_chart(size_data.set_index('Category'))

    with col2:
        st.write("**Storage Recommendations**")
        # Calculate estimated storage (assuming ~1KB per row)
        df['estimated_size_mb'] = (df['rows'] * 1024) / (1024 * 1024)
        total_storage = df['estimated_size_mb'].sum()
        st.metric("Total Estimated Storage", f"{total_storage:.1f} MB")

        if total_storage > 1000:  # More than 1GB
            st.warning("Consider archiving older datasets to free up storage")

# DATA GOVERNANCE RECOMMENDATIONS
st.subheader("Data Governance & Archiving Recommendations")

if not df.empty:
    # Get old datasets for archiving recommendations
    old_datasets = get_old_datasets()

    if old_datasets:
        st.warning("**Archiving Recommendations**")
        old_df = pd.DataFrame(old_datasets,
                              columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
        st.write(f"Found {len(old_df)} datasets older than 6 months:")
        st.dataframe(old_df[['name', 'upload_date', 'rows']])

        st.info(
            "Recommendation: Consider archiving these older datasets to improve performance and reduce storage costs")

    # Large datasets analysis
    large_datasets = get_large_datasets()
    if large_datasets:
        st.warning("**Large Dataset Management**")
        large_df = pd.DataFrame(large_datasets,
                                columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
        st.write(f"Found {len(large_df)} datasets with >10,000 rows:")
        st.dataframe(large_df[['name', 'rows', 'upload_date']])

        st.info("Recommendation: Monitor performance of large datasets and consider partitioning or compression")

# DATASET STATISTICS
st.subheader("Database Statistics")
try:
    stats = get_dataset_stats()
    if stats:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Datasets", stats[0])
        with col2:
            st.metric("Total Rows", f"{stats[1]:,}")
        with col3:
            st.metric("Average Rows", f"{stats[2]:,.0f}")
except:
    st.info("Could not load dataset statistics")

# MAIN DATA TABLE
st.subheader("All Datasets")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No datasets found")

# SEARCH AND SPECIAL QUERIES
st.sidebar.header("Special Queries")

if st.sidebar.button("Show Large Datasets (>10k rows)"):
    large_datasets = get_large_datasets()
    if large_datasets:
        large_df = pd.DataFrame(large_datasets,
                                columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
        st.subheader("Large Datasets (>10,000 rows)")
        st.dataframe(large_df)

if st.sidebar.button("Show Recent Uploads"):
    recent_datasets = get_recent_uploads(5)
    if recent_datasets:
        recent_df = pd.DataFrame(recent_datasets,
                                 columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
        st.subheader("Recent Dataset Uploads")
        st.dataframe(recent_df)

# USER DATASETS
st.sidebar.header("User Datasets")
username = st.sidebar.text_input("Enter username to view their datasets (uploaded by)")
if username:
    user_datasets = get_user_datasets(username)
    if user_datasets:
        user_df = pd.DataFrame(user_datasets,
                               columns=['dataset_id', 'name', 'rows', 'columns', 'uploaded_by', 'upload_date'])
        st.subheader(f"Datasets uploaded by {username}")
        st.dataframe(user_df)
    elif username:
        st.info(f"No datasets found for user: {username}")

