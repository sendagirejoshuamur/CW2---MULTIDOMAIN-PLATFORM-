import streamlit as st
import pandas as pd
from app.data.incidents import *

# Login check
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.stop()

st.set_page_config(page_title="Cyber Incidents", layout="wide")
st.title("Cyber Incidents Dashboard")

# Get data using crud functions from data.py
data = get_all_incidents()

# SIDEBAR FILTERS
st.sidebar.header("Filters")

# Date filter
if 'timestamp' in data.columns:
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    min_date = data['timestamp'].min().date()
    max_date = data['timestamp'].max().date()

    date_range = st.sidebar.date_input("Date Range", (min_date, max_date))
    if len(date_range) == 2:
        start_date, end_date = date_range
        data = data[(data['timestamp'].dt.date >= start_date) & (data['timestamp'].dt.date <= end_date)]

# Category filter
if 'category' in data.columns:
    category = st.sidebar.selectbox("Threat Category", ['All'] + list(data['category'].unique()))
    if category != 'All':
        data = data[data['category'] == category]

# Severity filter
if 'severity' in data.columns:
    severity = st.sidebar.selectbox("Severity", ['All'] + list(data['severity'].unique()))
    if severity != 'All':
        data = data[data['severity'] == severity]

# Status filter
if 'status' in data.columns:
    status = st.sidebar.selectbox("Status", ['All'] + list(data['status'].unique()))
    if status != 'All':
        data = data[data['status'] == status]

# QUICK STATS (using your database column names)
st.subheader("Quick Stats")
if not data.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Incidents", len(data))
    with col2:
        # Use your actual category column name
        if 'category' in data.columns:
            phishing_count = len(data[data['category'].str.contains('phishing', case=False, na=False)])
            st.metric("Phishing Incidents", phishing_count)
        else:
            st.metric("Phishing Incidents", 0)

# SIMPLE CHARTS
st.subheader("Charts")
if not data.empty:
    col1, col2 = st.columns(2)

    with col1:
        if 'category' in data.columns:
            st.write("By Category")
            category_counts = data['category'].value_counts()
            st.bar_chart(category_counts)

    with col2:
        if 'status' in data.columns:
            st.write("By Status")
            status_counts = data['status'].value_counts()
            st.bar_chart(status_counts)

    col3, col4 = st.columns(2)

    with col3:
        if 'severity' in data.columns:
            st.write("By Severity")
            severity_counts = data['severity'].value_counts()
            st.bar_chart(severity_counts)

    with col4:
        if 'timestamp' in data.columns:
            st.write("Over Time")
            daily_counts = data.groupby(data['timestamp'].dt.date).size()
            st.line_chart(daily_counts)

# USE YOUR STATS FUNCTION
st.subheader("Database Statistics")
try:
    stats_data = get_incident_stats()
    if not stats_data.empty:
        st.dataframe(stats_data)

        # Displaying stats in a more readable format
        st.write("**Summary by Severity and Status:**")
        for _, row in stats_data.iterrows():
            st.write(f"{row['severity']} severity - {row['status']}: {row['count']} incidents")
except:
    st.info("Could not load statistics from database")

# DATA TABLE
st.subheader("Incident Data")
st.dataframe(data)

# SEARCH FUNCTIONALITY USING YOUR FUNCTION
st.sidebar.header("Search")
search_term = st.sidebar.text_input("Search in descriptions")
if search_term:
    search_results = search_incidents(search_term)
    st.subheader(f"Search Results for '{search_term}'")
    st.dataframe(search_results)

# RECOMMENDATIONS
st.info("""
**Recommendations:**

1. **Prioritize High-Severity Incidents**: Focus resources on resolving high-severity incidents first to mitigate critical risks.

2. **Address Open Incidents**: Review and close open incidents to reduce your organization's attack surface.

3. **Phishing Prevention**: Since phishing appears to be a significant threat category, consider enhancing employee security awareness training.

4. **Trend Analysis**: Monitor the "Over Time" chart to identify seasonal patterns or spikes in incidents that may require additional resources.

5. **Proactive Filtering**: Use the sidebar filters to drill down into specific categories or severity levels for targeted analysis.

6. **Response Time Metrics**: Consider adding average resolution time metrics to track incident response efficiency.

7. **Pattern Detection**: Use the search functionality to identify recurring patterns or similar incidents that might indicate a coordinated attack.
""")