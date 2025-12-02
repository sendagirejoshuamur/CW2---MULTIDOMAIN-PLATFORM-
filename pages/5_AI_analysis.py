import streamlit as st
from google import genai
from google.genai import types
from app.data.incidents import *
from app.data.tickets import *
from app.data.datasets import *
import time


# Login check
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in first.")
    st.stop()


# Initialize Gemini AI client using API key from secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])


#  DATASETS ANALYSIS FUNCTION

def get_datasets_analysis():
    """
    Get datasets analysis options and retrieve data based on user selection
    Returns: option selected, context description, and raw data text
    """
    st.subheader("Dataset Analysis Options")

    # Dropdown menu for different dataset analysis options
    option = st.selectbox(
        "Choose analysis type:",
        [
            "Show all datasets",
            "Dataset statistics overview",
            "Large datasets (>10,000 rows)",
            "Old datasets (>6 months)",
            "My datasets (enter username)",
            "Search datasets"
        ]
    )

    data_context = ""  # Description of what data we're analyzing
    raw_data = ""  # Actual data to send to AI

    # Option 1: Get all datasets from database
    if option == "Show all datasets":
        datasets = get_all_datasets()
        if datasets:
            data_context = "Complete list of all datasets in the system"
            raw_data = f"Found {len(datasets)} datasets:\n"
            for ds in datasets[:15]:  # Limit to 15 to avoid too much data for AI
                raw_data += f"- ID: {ds[0]}, Name: {ds[1]}, Rows: {ds[2]}, Columns: {ds[3]}, Uploaded by: {ds[4]}, Date: {ds[5]}\n"
            if len(datasets) > 15:
                raw_data += f"... and {len(datasets) - 15} more datasets"
        else:
            raw_data = "No datasets found in the database."

    # Option 2: Get dataset statistics
    elif option == "Dataset statistics overview":
        stats = get_dataset_stats()
        if stats:
            data_context = "Statistical summary of all datasets"
            raw_data = f"""Dataset Statistics:
• Total datasets: {stats[0]}
• Total rows across all datasets: {stats[1]:,}
• Average rows per dataset: {stats[2]:,.0f}
• Largest datasets would be those over 10,000 rows
• Oldest datasets are over 6 months"""
        else:
            raw_data = "Could not retrieve dataset statistics."

    # Option 3: Get large datasets (over 10,000 rows)
    elif option == "Large datasets (>10,000 rows)":
        large_datasets = get_large_datasets()
        if large_datasets:
            data_context = "Large datasets that exceed 10,000 rows"
            raw_data = f"Found {len(large_datasets)} large datasets:\n"
            for ds in large_datasets:
                raw_data += f"- {ds[1]} has {ds[2]:,} rows and {ds[3]} columns (uploaded by {ds[4]} on {ds[5]})\n"
        else:
            raw_data = "No datasets with more than 10,000 rows found."

    # Option 4: Get old datasets (older than 6 months)
    elif option == "Old datasets (>6 months)":
        old_datasets = get_old_datasets()
        if old_datasets:
            data_context = "Datasets older than 6 months"
            raw_data = f"Found {len(old_datasets)} old datasets:\n"
            for ds in old_datasets:
                raw_data += f"- {ds[1]} was uploaded on {ds[5]} (has {ds[2]} rows)\n"
        else:
            raw_data = "No datasets older than 6 months found."

    # Option 5: Get datasets by specific user
    elif option == "My datasets (enter username)":
        username = st.text_input("Enter your username:")
        if username:
            user_datasets = get_user_datasets(username)
            if user_datasets:
                data_context = f"Datasets uploaded by user: {username}"
                raw_data = f"Found {len(user_datasets)} datasets:\n"
                for ds in user_datasets:
                    raw_data += f"- {ds[1]} ({ds[2]} rows, uploaded on {ds[5]})\n"
            else:
                raw_data = f"No datasets found for user '{username}'."

    # Option 6: Search datasets by name or uploader
    elif option == "Search datasets":
        search_term = st.text_input("Enter search term(name):")
        if search_term:
            all_datasets = get_all_datasets()
            if all_datasets:
                matched = [ds for ds in all_datasets if search_term.lower() in ds[1].lower() or
                           search_term.lower() in str(ds[4]).lower()]
                if matched:
                    data_context = f"Datasets matching search term: {search_term}"
                    raw_data = f"Found {len(matched)} datasets:\n"
                    for ds in matched:
                        raw_data += f"- {ds[1]} (uploaded by {ds[4]}, {ds[2]} rows)\n"
                else:
                    raw_data = f"No datasets found matching '{search_term}'."

    return option, data_context, raw_data


#  INCIDENTS ANALYSIS FUNCTION

def get_incidents_analysis():
    """
    Get security incidents analysis options and retrieve data
    Returns: option selected, context description, and raw data text
    """
    st.subheader("Security Incidents Analysis")

    # Dropdown menu for different incident analysis options
    option = st.selectbox(
        "Choose analysis type:",
        [
            "All incidents",
            "Incident statistics",
            "Incidents by severity",
            "Incidents by status",
            "Search incidents"
        ]
    )

    data_context = ""
    raw_data = ""

    # Option 1: Get all security incidents
    if option == "All incidents":
        df_incidents = get_all_incidents()
        if not df_incidents.empty:
            data_context = "All security incidents in the system"
            raw_data = f"Found {len(df_incidents)} incidents:\n"
            for idx, row in df_incidents.head(10).iterrows():
                raw_data += f"- Incident ID: {row.get('incident_id', 'N/A')}, Category: {row.get('category', 'N/A')}, Severity: {row.get('severity', 'N/A')}, Status: {row.get('status', 'N/A')}, Description: {row.get('description', 'No description')[:100]}\n"
            if len(df_incidents) > 10:
                raw_data += f"... and {len(df_incidents) - 10} more incidents"
        else:
            raw_data = "No incidents found in the database."

    # Option 2: Get incident statistics (counts by severity and status)
    elif option == "Incident statistics":
        df_stats = get_incident_stats()
        if not df_stats.empty:
            data_context = "Statistical breakdown of security incidents"
            raw_data = "Incident Statistics:\n"
            for idx, row in df_stats.iterrows():
                raw_data += f"- Severity: {row['severity']}, Status: {row['status']}, Count: {row['count']}\n"
        else:
            raw_data = "Could not retrieve incident statistics."

    # Option 3: Filter incidents by severity level
    elif option == "Incidents by severity":
        severity = st.selectbox("Select severity:", ["Critical", "High", "Medium", "Low"])
        if severity:
            df_incidents = get_incident_by_severity(severity)
            if not df_incidents.empty:
                data_context = f"Security incidents with {severity} severity"
                raw_data = f"Found {len(df_incidents)} {severity} severity incidents:\n"
                for idx, row in df_incidents.head(10).iterrows():
                    raw_data += f"- Category: {row.get('category', 'N/A')}, Status: {row.get('status', 'N/A')}, Description: {row.get('description', 'No description')[:80]}\n"
            else:
                raw_data = f"No {severity} severity incidents found."

    # Option 4: Filter incidents by status
    elif option == "Incidents by status":
        status = st.selectbox("Select status:", ["Open", "In Progress", "Closed", "Resolved"])
        if status:
            df_incidents = get_incidents_by_status(status)
            if not df_incidents.empty:
                data_context = f"Security incidents with status: {status}"
                raw_data = f"Found {len(df_incidents)} incidents with status '{status}':\n"
                for idx, row in df_incidents.head(10).iterrows():
                    raw_data += f"- Severity: {row.get('severity', 'N/A')}, Category: {row.get('category', 'N/A')}, Description: {row.get('description', 'No description')[:80]}\n"
            else:
                raw_data = f"No incidents found with status '{status}'."

    # Option 5: Search incidents by description
    elif option == "Search incidents":
        search_term = st.text_input("Search in incident descriptions:")
        if search_term:
            df_incidents = search_incidents(search_term)
            if not df_incidents.empty:
                data_context = f"Incidents matching search: {search_term}"
                raw_data = f"Found {len(df_incidents)} incidents:\n"
                for idx, row in df_incidents.head(10).iterrows():
                    raw_data += f"- Severity: {row.get('severity', 'N/A')}, Status: {row.get('status', 'N/A')}, Description: {row.get('description', 'No description')}\n"
            else:
                raw_data = f"No incidents found matching '{search_term}'."

    return option, data_context, raw_data


#  TICKETS ANALYSIS FUNCTION

def get_tickets_analysis():
    """
    Get IT tickets analysis options and retrieve data
    Returns: option selected, context description, and raw data text
    """
    st.subheader("IT Tickets Analysis")

    # Dropdown menu for different ticket analysis options
    option = st.selectbox(
        "Choose analysis type:",
        [
            "All tickets",
            "Bottleneck analysis",
            "Tickets by assignee",
            "Tickets by status",
            "Oldest pending tickets"
        ]
    )

    data_context = ""
    raw_data = ""

    # Option 1: Get all IT tickets
    if option == "All tickets":
        tickets = get_all_tickets()
        if tickets:
            data_context = "All IT tickets in the system"
            raw_data = f"Found {len(tickets)} tickets:\n"
            for ticket in tickets[:10]:
                raw_data += f"- Ticket ID: {ticket[0]}, Priority: {ticket[1]}, Status: {ticket[3]}, Assigned to: {ticket[4]}, Created: {ticket[5]}, Description: {ticket[2][:80]}\n"
            if len(tickets) > 10:
                raw_data += f"... and {len(tickets) - 10} more tickets"
        else:
            raw_data = "No tickets found in the database."

    # Option 2: Analyze bottlenecks in ticket processing
    elif option == "Bottleneck analysis":
        # Get three types of bottleneck data
        slow_status = get_slowest_status()  # Tickets stuck by status
        slow_staff = get_slowest_staff()  # Staff with most unresolved tickets
        avg_time = get_avg_resolution_time()  # Average resolution time by priority

        data_context = "IT ticket bottlenecks and performance issues"
        raw_data = "Bottleneck Analysis:\n\n"

        raw_data += "Status Bottlenecks:\n"
        if slow_status:
            for status, count in slow_status:
                raw_data += f"- {status}: {count} unresolved tickets\n"
        else:
            raw_data += "- No status bottleneck data\n"

        raw_data += "\nStaff Workload:\n"
        if slow_staff:
            for staff, count in slow_staff:
                raw_data += f"- {staff}: {count} unresolved tickets\n"
        else:
            raw_data += "- No staff workload data\n"

        raw_data += "\nResolution Times:\n"
        if avg_time:
            for priority, hours in avg_time:
                raw_data += f"- {priority} priority: {hours:.1f} hours average\n"

    # Option 3: Filter tickets by assigned staff member
    elif option == "Tickets by assignee":
        assignee = st.text_input("Enter staff member name:")
        if assignee:
            tickets = get_tickets_by_assignee(assignee)
            if tickets:
                data_context = f"Tickets assigned to: {assignee}"
                raw_data = f"Found {len(tickets)} tickets:\n"
                for ticket in tickets[:10]:
                    raw_data += f"- Ticket ID: {ticket[0]}, Priority: {ticket[1]}, Status: {ticket[3]}, Created: {ticket[5]}\n"
            else:
                raw_data = f"No tickets found assigned to '{assignee}'."

    # Option 4: Filter tickets by status
    elif option == "Tickets by status":
        status = st.selectbox("Select ticket status:", ["Open", "In Progress", "Pending", "Resolved"])
        if status:
            tickets = get_tickets_by_status(status)
            if tickets:
                data_context = f"Tickets with status: {status}"
                raw_data = f"Found {len(tickets)} tickets:\n"
                for ticket in tickets[:10]:
                    raw_data += f"- Ticket ID: {ticket[0]}, Priority: {ticket[1]}, Assigned to: {ticket[4]}, Created: {ticket[5]}\n"
            else:
                raw_data = f"No tickets found with status '{status}'."

    # Option 5: Get oldest unresolved tickets
    elif option == "Oldest pending tickets":
        tickets = get_oldest_pending_tickets(10)
        if tickets:
            data_context = "Oldest unresolved tickets"
            raw_data = "Oldest pending tickets:\n"
            for ticket in tickets:
                raw_data += f"- Ticket #{ticket[0]} created on {ticket[5]}, Priority: {ticket[1]}, Status: {ticket[3]}, Assigned to: {ticket[4]}\n"
        else:
            raw_data = "No pending tickets found."

    return option, data_context, raw_data


#  AI ANALYSIS FUNCTION

def analyze_with_ai_simple(data_type, analysis_type, data_context, raw_data):
    """
    Send data to Gemini AI for analysis with retry logic
    Parameters:
        data_type: Type of data (Datasets, Incidents, Tickets)
        analysis_type: Specific analysis option selected
        data_context: Description of what data contains
        raw_data: Actual data text to analyze
    Returns: AI response text or fallback message
    """

    # Set AI role and focus areas based on data type
    if "Datasets" in data_type:
        system_role = "dataset management and data governance expert"
        focus_areas = "data storage efficiency, data freshness, user activity patterns, and data governance policies"
    elif "Incidents" in data_type:
        system_role = "cyber security incident response expert"
        focus_areas = "security risks, incident patterns, response effectiveness, and threat mitigation"
    else:  # Tickets
        system_role = "IT service management and ticketing system expert"
        focus_areas = "service delivery efficiency, staff workload, resolution times, and process bottlenecks"

    # Create prompt for AI with structured instructions
    prompt = f"""
    You are a {system_role}. Analyze this data and provide specific insights.

    ANALYSIS REQUEST: {analysis_type}
    CONTEXT: {data_context}

    DATA TO ANALYZE:
    {raw_data}

    Please provide a concise analysis focusing on:
    1. KEY FINDINGS - What are the main patterns or issues?
    2. RISK ASSESSMENT - What are the potential risks or problems?
    3. RECOMMENDATIONS - What specific actions should be taken?
    4. PRIORITIES - What needs immediate attention?

    Focus on {focus_areas}. Keep it practical and actionable.
    """

    # Try API call with retry logic (helps with temporary failures)
    max_retries = 2
    for attempt in range(max_retries):
        try:
            # Send request to Gemini AI
            response = client.models.generate_content(
                model="gemini-2.0-flash",  # Use faster model (less likely to be overloaded)
                config=types.GenerateContentConfig(
                    system_instruction=f"You are {system_role}. Provide practical, actionable insights."),
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            return response.text  # Return AI analysis

        except Exception as e:
            # If API fails, wait and retry once
            if attempt < max_retries - 1:
                time.sleep(1)  # Wait 1 second before retry
                continue
            else:
                # If all retries fail, provide fallback message
                return f"""
                AI Service Temporarily Unavailable

                Based on the {analysis_type} data provided:

                Quick Analysis:
                - You're analyzing: {data_context}
                - Data shows: {len(raw_data.split('\\n'))} data points

                Suggested Next Steps:
                1. Review the raw data in the expander above
                2. Look for patterns in status, priority, or dates
                3. Check for any urgent items needing attention
                4. Try the AI analysis again in a few minutes

                Manual Analysis Tips:
                - Count items by category/status
                - Look for oldest items
                - Identify any bottlenecks or risks
                - Note patterns in assignments or uploads
                """

    return "Unable to analyze at this time. Please try again later."


#  MAIN APPLICATION

def main():
    """
    Main Streamlit application function
    Controls the user interface and flow
    """
    # Configure page settings
    st.set_page_config(
        page_title="Simple Data Analyzer",
        page_icon="",
        layout="centered"
    )

    st.title("Data Analysis Assistant")

    # Step 1: User selects what type of data to analyze
    data_type = st.radio(
        "What would you like to analyze?",
        ["Datasets", "Security Incidents", "IT Tickets"],
        horizontal=True
    )

    # Get analysis based on user selection
    analysis_type = ""
    data_context = ""
    raw_data = ""

    if data_type == "Datasets":
        analysis_type, data_context, raw_data = get_datasets_analysis()
    elif data_type == "Security Incidents":
        analysis_type, data_context, raw_data = get_incidents_analysis()
    else:  # Tickets
        analysis_type, data_context, raw_data = get_tickets_analysis()

    # Show preview of data before sending to AI
    if raw_data:
        st.subheader("Data Preview")
        with st.expander("View raw data", expanded=False):
            st.text(raw_data[:500] + "..." if len(raw_data) > 500 else raw_data)

    # Step 2: Analyze button (only enabled if we have data)
    if st.button("Analyze with AI", type="primary", disabled=not raw_data):
        with st.spinner("Analyzing data with AI..."):
            # Get AI analysis
            ai_response = analyze_with_ai_simple(data_type, analysis_type, data_context, raw_data)

            # Display results
            st.markdown("---")
            st.subheader("AI Analysis Results")

            # Store analysis in session state for history
            if 'analyses' not in st.session_state:
                st.session_state.analyses = []

            analysis_entry = {
                'data_type': data_type,
                'analysis_type': analysis_type,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'ai_response': ai_response,
                'data_preview': raw_data[:200] + "..." if len(raw_data) > 200 else raw_data
            }

            st.session_state.analyses.append(analysis_entry)

            # Show AI analysis
            st.markdown(ai_response)

            # Option to view full raw data
            with st.expander("View Full Raw Data", expanded=False):
                st.text(raw_data)

    # Step 3: Show analysis history (last 5 analyses)
    if 'analyses' in st.session_state and st.session_state.analyses:
        st.markdown("---")
        st.subheader("Analysis History")

        for i, analysis in enumerate(reversed(st.session_state.analyses[-5:])):
            with st.expander(f"{analysis['data_type']} - {analysis['analysis_type']} ({analysis['timestamp']})",
                             expanded=(i == 0)):
                st.markdown(analysis['ai_response'])
                with st.expander("View data used"):
                    st.text(analysis['data_preview'])

    # Clear history button
    if st.button("Clear History", type="secondary"):
        if 'analyses' in st.session_state:
            st.session_state.analyses = []
        st.rerun()


# Start the application
if __name__ == "__main__":
    main()