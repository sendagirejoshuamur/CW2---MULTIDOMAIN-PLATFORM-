from app.data.incidents import *
from app.data.tickets import *
from app.data.datasets import *
import streamlit as st
from app.data.users import *
from app.data.csv_loaders import *
from app.services.user_service import *
from pathlib import Path
import pandas as pd

# PAGE CONFIG
st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


#  AUTHENTICATION CHECK
def check_admin_access():
    """Check if user is logged in and has admin privileges"""
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        return False

    # Check if user has admin privileges
    if st.session_state.get('is_admin', False):
        return True

    # Also check user_role for backward compatibility
    if st.session_state.get('user_role') == 'admin':
        return True

    return False


# MAIN CONTENT
if not check_admin_access():
    st.title("Access Denied")
    st.error("You must be logged in as an administrator to access this panel.")

    if st.button("Go to Login"):
        try:
            st.switch_page("login.py")
        except:
            st.switch_page("login.py")

else:
    #SIDEBAR
    st.sidebar.title("Admin Panel")
    st.sidebar.markdown("BEST SIDE OF THE PAGE")

    # Display user info in sidebar
    username = st.session_state.get('username', 'Admin')

    st.sidebar.write(f"Welcome, **{username}**")

    if st.sidebar.button("Logout"):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    menu = st.sidebar.radio("Navigation", ["Dashboard", "incidents", "tickets", "datasets", "users", "clear Database"])

    # Rest of your admin panel code remains exactly the same...
    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.title("Admin Dashboard")
        st.write("Welcome to the admin dashboard!")
        st.info("You can manage all aspects of the platform.")
        st.write("You can also view statistics about your platform.")
        st.write("Choose action from the sidebar to get started!")

        # Quick stats or overview can go here
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Users", len(get_all_users()))
        with col2:
            st.metric("Total Incidents", len(get_all_incidents()))
        with col3:
            st.metric("Total Tickets", len(get_all_tickets()))

    # --- INCIDENTS MANAGEMENT ---
    if menu == "incidents":
        st.title("Cyber Incidents Management")

        st.sidebar.subheader("Incident Actions")
        incident_action = st.sidebar.radio(
            "Choose Action",
            ["View All", "Add Incident", "Update Status", "Delete Incident", "Filter by Status", "Search", "Statistics"]
        )

        #  VIEW ALL INCIDENTS
        if incident_action == "View All":
            st.subheader("All Incidents")
            df = get_all_incidents()
            st.dataframe(df)

        #  ADD INCIDENT
        elif incident_action == "Add Incident":
            st.subheader("Add New Incident")
            with st.form("incident_form"):
                incident_id = st.text_input("Incident ID")
                timestamp = st.text_input("Timestamp (YYYY-MM-DD HH:MM:SS)")
                severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
                category = st.text_input("Category")
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
                description = st.text_area("Description")
                reported_by = st.text_input("Reported By")
                submitted = st.form_submit_button("Add Incident")

                if submitted:
                    new_id = insert_incident(
                        incident_id, timestamp, severity, category, status, description, reported_by
                    )
                    st.success(f"Incident added with ID: {new_id}")

        #  UPDATE STATUS
        elif incident_action == "Update Status":
            st.subheader("Update Incident Status")
            incident_id = st.text_input("Incident Database ID")
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
            if st.button("Update Status"):
                rows = update_incident_status(incident_id, new_status)
                if rows:
                    st.success("Incident status updated successfully")
                else:
                    st.error("Incident not found")

        #  DELETE INCIDENT
        elif incident_action == "Delete Incident":
            st.subheader("Delete Incident")
            incident_id = st.text_input("Incident Database ID to Delete")
            if st.button("Delete Incident"):
                rows = delete_incident(incident_id)
                if rows:
                    st.success("Incident deleted successfully")
                else:
                    st.error("Incident not found")

        #  FILTER BY STATUS
        elif incident_action == "Filter by Status":
            st.subheader("Filter Incidents by Status")
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            df = get_incidents_by_status(status)
            st.dataframe(df)

        #  SEARCH INCIDENTS
        elif incident_action == "Search":
            st.subheader("Search Incidents by Description")
            term = st.text_input("Search Term")
            if st.button("Search"):
                df = search_incidents(term)
                st.dataframe(df)

        #  INCIDENT STATISTICS
        elif incident_action == "Statistics":
            st.subheader("Incident Statistics by Severity and Status")
            df = get_incident_stats()
            st.dataframe(df)

            st.subheader("Visualize Statistics")
            chart_data = df.pivot(index="severity", columns="status", values="count").fillna(0)
            st.bar_chart(chart_data)

    # --- TICKETS MANAGEMENT ---
    elif menu == "tickets":
        st.title("Tickets Management")

        st.sidebar.subheader("Ticket Actions")
        ticket_action = st.sidebar.radio(
            "Choose Action",
            ["View All", "Add Ticket", "Update Status", "Assign Ticket", "Delete Ticket", "Filter by Status",
             "Filter by Assignee", "Analysis"]
        )

        #  VIEW ALL TICKETS
        if ticket_action == "View All":
            st.subheader("All Tickets")
            tickets = get_all_tickets()
            df = pd.DataFrame(tickets,
                              columns=["Ticket ID", "Priority", "Description", "Status", "Assigned To", "Created At",
                                       "Resolution Time (hrs)"])
            st.dataframe(df)

        #  ADD TICKET
        elif ticket_action == "Add Ticket":
            st.subheader("Add New Ticket")
            with st.form("ticket_form"):
                ticket_id = st.text_input("Ticket ID")
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
                description = st.text_area("Description")
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
                assigned_to = st.text_input("Assigned To (Optional)")
                created_at = st.text_input("Created At (YYYY-MM-DD HH:MM:SS)")
                resolution_time = st.number_input("Resolution Time (hours, optional)", min_value=0.0)
                submitted = st.form_submit_button("Add Ticket")

                if submitted:
                    insert_into_tickets(ticket_id, priority, description, status, assigned_to, created_at,
                                        resolution_time)
                    st.success(f"Ticket {ticket_id} added successfully")

        #  UPDATE STATUS
        elif ticket_action == "Update Status":
            st.subheader("Update Ticket Status")
            ticket_id = st.text_input("Ticket ID")
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved"])
            if st.button("Update Status"):
                update_ticket_status(ticket_id, new_status)
                st.success(f"Ticket {ticket_id} status updated to {new_status}")

        #  ASSIGN TICKET
        elif ticket_action == "Assign Ticket":
            st.subheader("Assign Ticket to Staff")
            ticket_id = st.text_input("Ticket ID")
            staff = st.text_input("Assign to")
            if st.button("Assign Ticket"):
                assign_ticket(ticket_id, staff)
                st.success(f"Ticket {ticket_id} assigned to {staff}")

        #  DELETE TICKET
        elif ticket_action == "Delete Ticket":
            st.subheader("Delete Ticket")
            ticket_id = st.text_input("Ticket ID to Delete")
            if st.button("Delete Ticket"):
                rows = delete_tickets(ticket_id)
                if rows:
                    st.success(f"Ticket {ticket_id} deleted successfully")
                else:
                    st.error("Ticket not found")

        #  FILTER BY STATUS
        elif ticket_action == "Filter by Status":
            st.subheader("Filter Tickets by Status")
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            tickets = get_tickets_by_status(status)
            df = pd.DataFrame(tickets,
                              columns=["Ticket ID", "Priority", "Description", "Status", "Assigned To", "Created At",
                                       "Resolution Time (hrs)"])
            st.dataframe(df)

        #  FILTER BY ASSIGNEE
        elif ticket_action == "Filter by Assignee":
            st.subheader("Filter Tickets by Staff")
            staff = st.text_input("Assigned To")
            tickets = get_tickets_by_assignee(staff)
            df = pd.DataFrame(tickets,
                              columns=["Ticket ID", "Priority", "Description", "Status", "Assigned To", "Created At",
                                       "Resolution Time (hrs)"])
            st.dataframe(df)

        #  ANALYSIS
        elif ticket_action == "Analysis":
            st.subheader("Ticket Analysis / Bottlenecks")

            # Slowest status
            st.markdown("**Status with most unresolved tickets:**")
            slow_status = get_slowest_status()
            df_status = pd.DataFrame(slow_status, columns=["Status", "Ticket Count"])
            st.dataframe(df_status)

            # Slowest staff
            st.markdown("**Staff with most unresolved tickets:**")
            slow_staff = get_slowest_staff()
            df_staff = pd.DataFrame(slow_staff, columns=["Staff", "Ticket Count"])
            st.dataframe(df_staff)

            # Average resolution time
            st.markdown("**Average resolution time by priority:**")
            avg_res = get_avg_resolution_time()
            df_avg = pd.DataFrame(avg_res, columns=["Priority", "Avg Resolution Time (hrs)"])
            st.dataframe(df_avg)

            # Oldest pending tickets
            st.markdown("**Oldest unresolved tickets:**")
            old_tickets = get_oldest_pending_tickets(limit=10)
            df_old = pd.DataFrame(old_tickets,
                                  columns=["Ticket ID", "Priority", "Description", "Status", "Assigned To",
                                           "Created At",
                                           "Resolution Time (hrs)"])
            st.dataframe(df_old)

    # --- DATASETS MANAGEMENT ---
    elif menu == "datasets":
        st.title("Datasets Management")

        st.sidebar.subheader("Dataset Actions")
        dataset_action = st.sidebar.radio(
            "Choose Action",
            ["View All", "Add Dataset", "Delete Dataset", "Filter by User", "Large Datasets", "Old Datasets",
             "Statistics",
             "Recent Uploads"]
        )

        #  VIEW ALL DATASETS
        if dataset_action == "View All":
            st.subheader("All Datasets")
            datasets = get_all_datasets()
            df = pd.DataFrame(datasets, columns=["Dataset ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"])
            st.dataframe(df)

        #  ADD DATASET
        elif dataset_action == "Add Dataset":
            st.subheader("Add New Dataset Metadata")
            with st.form("dataset_form"):
                dataset_id = st.text_input("Dataset ID")
                name = st.text_input("Dataset Name")
                rows = st.number_input("Rows", min_value=0)
                columns = st.number_input("Columns", min_value=0)
                uploaded_by = st.text_input("Uploaded By")
                upload_date = st.text_input("Upload Date (YYYY-MM-DD)")
                submitted = st.form_submit_button("Add Dataset")

                if submitted:
                    insert_into_datasets(dataset_id, name, rows, columns, uploaded_by, upload_date)
                    st.success(f"Dataset {name} added successfully")

        #  DELETE DATASET
        elif dataset_action == "Delete Dataset":
            st.subheader("Delete Dataset")
            dataset_id = st.text_input("Dataset ID to Delete")
            if st.button("Delete Dataset"):
                delete_from_datasets(dataset_id)
                st.success(f"Dataset {dataset_id} deleted successfully")

        #  FILTER BY USER
        elif dataset_action == "Filter by User":
            st.subheader("Datasets Uploaded by User")
            user = st.text_input("Username")
            datasets = get_user_datasets(user)
            df = pd.DataFrame(datasets, columns=["Dataset ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"])
            st.dataframe(df)

        #  LARGE DATASETS
        elif dataset_action == "Large Datasets":
            st.subheader("Datasets with More Than 10,000 Rows")
            datasets = get_large_datasets()
            df = pd.DataFrame(datasets, columns=["Dataset ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"])
            st.dataframe(df)

        #  OLD DATASETS
        elif dataset_action == "Old Datasets":
            st.subheader("Datasets Older than 6 Months")
            datasets = get_old_datasets()
            df = pd.DataFrame(datasets, columns=["Dataset ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"])
            st.dataframe(df)

        #  DATASET STATISTICS
        elif dataset_action == "Statistics":
            st.subheader("Dataset Statistics")
            stats = get_dataset_stats()
            st.write(f"**Total Datasets:** {stats[0]}")
            st.write(f"**Total Rows Across All Datasets:** {stats[1]}")
            st.write(f"**Average Rows Per Dataset:** {stats[2]:.2f}")

        #  RECENT UPLOADS
        elif dataset_action == "Recent Uploads":
            st.subheader("Most Recent Dataset Uploads")
            datasets = get_recent_uploads(limit=10)
            df = pd.DataFrame(datasets, columns=["Dataset ID", "Name", "Rows", "Columns", "Uploaded By", "Upload Date"])
            st.dataframe(df)

    # --- USERS MANAGEMENT ---
    elif menu == "users":
        st.title("Users Management")

        st.sidebar.subheader("User Actions")
        user_action = st.sidebar.radio(
            "Choose Action",
            ["View All Users", "Add User", "Clear Users Table"]
        )

        #  VIEW ALL USERS
        if user_action == "View All Users":
            st.subheader("All Users")
            users = get_all_users()
            # Assuming your DB stores hashed passwords but you want original password
            # If you store original passwords, replace password_hash with that column
            df = pd.DataFrame(users, columns=["ID", "Username", "Password Hash", "Role"])
            st.dataframe(df)

        #  ADD USER
        elif user_action == "Add User":
            st.subheader("Add New User")
            st.subheader("migrate users from file")

            if st.button("migrate all users to database"):
                migrate_users_from_file()
                st.success("users migrated successfully")

            if st.button("add user manually"):
                with st.form("add_user_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    role = st.selectbox("Role", ["user", "admin"])
                    submitted = st.form_submit_button("Add User")

                    if submitted:
                        # Hash the password
                        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                        # Store user with hash
                        insert_user(username, password_hash, role)
                        st.success(f"User {username} added successfully")
                        st.info(f"Original Password (for display purposes only): {password}")

        #  CLEAR USERS TABLE
        elif user_action == "Clear Users Table":
            st.subheader("Clear All Users")
            if st.button("Clear Users"):
                clear_users_table()
                st.success("Users table cleared and ID counter reset")

    #CLEAR DATABASE
    elif menu == "clear Database":
        st.title("Clear Database")
        st.warning("This action will permanently delete all data from all tables")
        st.write("Check the box below to confirm that you understand the consequences:")

        confirm_clear = st.checkbox("this actually works dont be stupid but anyway just give me my first class(-_-)")

        if confirm_clear:
            st.info("this actually works dont be stupid but anyway just give me my first class(-_-)")
            if st.button("Clear Database Now"):
                success = clear_database()
                if success:
                    st.success("All tables have been cleared and IDs reset successfully.")
                else:
                    st.error("Failed to clear the database. Check logs for details.")

        st.subheader("retrive info")

        if st.button("Retrieve Info"):

            conn = connect_database()

            st.info("Loading data from CSV files into database...")

            # Capture details per table
            data_dir = Path("DATA")
            csv_mappings = {
                'cyber_incidents.csv': 'cyber_incidents',
                'datasets_metadata.csv': 'datasets_metadata',
                'it_tickets.csv': 'it_tickets'
            }

            total_rows = 0
            table_details = []

            for csv_file, table_name in csv_mappings.items():
                csv_path = data_dir / csv_file
                if csv_path.exists():
                    rows_loaded = load_csv_to_table(conn, csv_path, table_name)
                    total_rows += rows_loaded
                    table_details.append((table_name, rows_loaded))
                else:
                    table_details.append((table_name, "CSV not found"))

            conn.close()

            # Display details in a table
            st.subheader("CSV Load Details")
            df_details = pd.DataFrame(table_details, columns=["Table Name", "Rows Loaded"])
            st.dataframe(df_details)

            st.success(f"All CSV files processed. Total rows loaded across all tables: {total_rows}")