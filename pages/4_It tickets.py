import streamlit as st
import pandas as pd
from app.data.tickets import *

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access this page.")
    st.stop()

st.set_page_config(page_title="IT Tickets", layout="wide")
st.title("IT Tickets Dashboard")

# Get all tickets from my crud function in tickets.py
tickets = get_all_tickets()

# Convert to DataFrame
if tickets:
    df = pd.DataFrame(tickets, columns=['ticket_id', 'priority', 'description', 'status', 'assigned_to', 'created_at',
                                        'resolution_time_hours'])
else:
    df = pd.DataFrame()

# QUICK STATS
st.subheader("Quick Stats")
if not df.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tickets", len(df))

    with col2:
        open_count = len(df[df['status'] != 'Resolved'])
        st.metric("Open Tickets", open_count)

    with col3:
        unassigned = len(df[df['assigned_to'].isna()])
        st.metric("Unassigned", unassigned)

# BOTTLENECK ANALYSIS
st.subheader("Bottlenecks")

# Show slowest status
slow_status = get_slowest_status()
if slow_status:
    status_df = pd.DataFrame(slow_status, columns=['Status', 'Count'])
    st.write("**Tickets stuck by status:**")
    st.dataframe(status_df)

# Show slowest staff
slow_staff = get_slowest_staff()
if slow_staff:
    staff_df = pd.DataFrame(slow_staff, columns=['Staff', 'Count'])
    st.write("**Staff workload:**")
    st.dataframe(staff_df)

# SIMPLE CHARTS
st.subheader("Charts")
if not df.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.write("By Status")
        status_counts = df['status'].value_counts()
        st.bar_chart(status_counts)

    with col2:
        st.write("By Priority")
        priority_counts = df['priority'].value_counts()
        st.bar_chart(priority_counts)

# TICKET TABLE
st.subheader("All Tickets")
if not df.empty:
    st.dataframe(df)
else:
    st.info("No tickets found")

# RECOMMENDATIONS
st.info("""
**Recommendations:**

1. **Address Unassigned Tickets**: Consider assigning the unassigned tickets to available staff members to prevent delays.

2. **Monitor Bottlenecks**: Focus on resolving tickets in the slowest status and support staff with the highest workload.

3. **Priority Management**: Ensure high-priority tickets are being addressed promptly by reviewing their current status.

4. **Workload Balancing**: Redistribute tickets among staff members to balance workload and improve resolution times.

5. **Regular Review**: Schedule weekly reviews of open tickets to identify aging issues that need escalation.
""")