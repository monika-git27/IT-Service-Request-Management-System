
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

# --------------------------------------------------
# 1. APPLICATION CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IT Service Management",
    page_icon="🎫",
    layout="wide"
)

st.title("IT Service Request Management System")
st.caption("A simple digital solution for managing employee IT support requests.")

# Locate the CSV file in the same folder as app.py
CSV_PATH = Path(__file__).with_name("it_service_requests.csv")

# Required dataset columns
COLUMNS = [
    "Ticket_ID",
    "Request_Date",
    "Employee_ID",
    "Department",
    "Request_Category",
    "Description",
    "Priority",
    "Assigned_Team",
    "Status",
    "Resolution_Date",
    "Resolution_Time_Hours"
]

# Category-to-team mapping
TEAM_MAP = {
    "Hardware": "IT Hardware Support",
    "Software": "Application Support",
    "Network": "Network Support",
    "Access": "Identity & Access Support"
}

# Demonstration SLA thresholds 
SLA_HOURS = {
    "High": 24,
    "Medium": 48,
    "Low": 72
}

# --------------------------------------------------
# 2. LOAD AND VALIDATE DATA
# --------------------------------------------------

def load_data():

    if not CSV_PATH.exists():
        st.error("CSV file not found. Place it beside app.py.")
        st.stop()

    data = pd.read_csv(CSV_PATH, dtype={"Ticket_ID": str})

    missing_columns = [
        column for column in COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.stop()

    data = data[COLUMNS].copy()

    data["Request_Date"] = pd.to_datetime(
        data["Request_Date"], errors="coerce"
    )

    data["Resolution_Date"] = pd.to_datetime(
        data["Resolution_Date"], errors="coerce"
    )

    data["Resolution_Time_Hours"] = pd.to_numeric(
        data["Resolution_Time_Hours"], errors="coerce"
    )

    return data


def save_data(data):

    data[COLUMNS].to_csv(CSV_PATH, index=False)


df = load_data()

# --------------------------------------------------
# 3. GENERATE UNIQUE TICKET ID
# --------------------------------------------------

def generate_ticket_id(data):

    if data.empty:
        next_number = 1

    else:
        numbers = pd.to_numeric(
            data["Ticket_ID"].str.extract(r"(\d+)$")[0],
            errors="coerce"
        )

        next_number = int(numbers.max()) + 1

    return f"IT{next_number:05d}"


# --------------------------------------------------
# 4. CALCULATE OVERDUE TICKETS
# --------------------------------------------------

def calculate_overdue(data):

    result = data.copy()

    current_time = pd.Timestamp.now()

    elapsed_hours = (
        current_time - result["Request_Date"]
    ).dt.total_seconds() / 3600

    allowed_hours = result["Priority"].map(SLA_HOURS)

    result["Overdue"] = (
        result["Status"].ne("Resolved")
        & elapsed_hours.gt(allowed_hours)
    )

    return result


df = calculate_overdue(df)

# --------------------------------------------------
# 5. APPLICATION NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Submit Request",
        "Manage Tickets",
        "All Tickets"
    ]
)

# --------------------------------------------------
# 6. DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.header("IT Service Performance Dashboard")

    total_tickets = len(df)

    open_tickets = (df["Status"] == "Open").sum()

    in_progress = (
        df["Status"] == "In Progress"
    ).sum()

    resolved = (
        df["Status"] == "Resolved"
    ).sum()

    overdue = df["Overdue"].sum()

    avg_resolution = (
        df.loc[
            df["Status"] == "Resolved",
            "Resolution_Time_Hours"
        ].mean()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Tickets", total_tickets)
    col2.metric("Open Tickets", open_tickets)
    col3.metric("In Progress", in_progress)

    col4, col5, col6 = st.columns(3)

    col4.metric("Resolved Tickets", resolved)
    col5.metric("Overdue Tickets", overdue)

    col6.metric(
        "Avg. Resolution Hours",
        f"{avg_resolution:.2f}"
        if pd.notna(avg_resolution)
        else "N/A"
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Tickets by Status")

        status_data = df["Status"].value_counts()

        st.bar_chart(status_data)

    with right:

        st.subheader("Tickets by Category")

        category_data = (
            df["Request_Category"].value_counts()
        )

        st.bar_chart(category_data)

    st.subheader("Tickets by Priority")

    priority_data = df["Priority"].value_counts()

    st.bar_chart(priority_data)

    st.subheader("Overdue Tickets")

    overdue_data = df[df["Overdue"]]

    if overdue_data.empty:

        st.success("No overdue tickets.")

    else:

        st.dataframe(
            overdue_data[
                [
                    "Ticket_ID",
                    "Priority",
                    "Request_Category",
                    "Status",
                    "Request_Date"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

# --------------------------------------------------
# 7. SUBMIT NEW REQUEST
# --------------------------------------------------

elif page == "Submit Request":

    st.header("Submit an IT Support Request")

    with st.form("request_form"):

        employee_id = st.text_input(
            "Employee ID",
            placeholder="Example: EMP0121"
        )

        department = st.selectbox(
            "Department",
            [
                "Finance",
                "Human Resources",
                "Sales",
                "Operations",
                "Marketing",
                "IT",
                "Customer Service",
                "Legal"
            ]
        )

        category = st.selectbox(
            "Request Category",
            ["Hardware", "Software", "Network", "Access"]
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"]
        )

        description = st.text_area(
            "Describe the IT issue",
            placeholder="Explain the problem..."
        )

        submitted = st.form_submit_button(
            "Submit Request"
        )

        if submitted:

            if not employee_id.strip() or not description.strip():

                st.error(
                    "Please enter Employee ID and issue description."
                )

            else:

                # Create new request
                new_ticket = {
                    "Ticket_ID": generate_ticket_id(df),
                    "Request_Date": pd.Timestamp.now(),
                    "Employee_ID": employee_id.strip().upper(),
                    "Department": department,
                    "Request_Category": category,
                    "Description": description.strip(),
                    "Priority": priority,
                    "Assigned_Team": TEAM_MAP[category],
                    "Status": "Open",
                    "Resolution_Date": pd.NaT,
                    "Resolution_Time_Hours": float("nan")
                }

                new_row = pd.DataFrame([new_ticket])

                updated_data = pd.concat(
                    [df, new_row],
                    ignore_index=True
                )

                save_data(updated_data)

                st.success(
                    f"Request submitted successfully! "
                    f"Ticket ID: {new_ticket['Ticket_ID']}"
                )

                st.info(
                    f"Assigned Team: {TEAM_MAP[category]}"
                )

# --------------------------------------------------
# 8. MANAGE EXISTING TICKETS
# --------------------------------------------------

elif page == "Manage Tickets":

    st.header("Manage IT Support Tickets")

    if df.empty:

        st.info("No tickets available.")

    else:

        ticket_id = st.selectbox(
            "Select Ticket ID",
            df["Ticket_ID"].tolist()
        )

        selected_ticket = df[
            df["Ticket_ID"] == ticket_id
        ].iloc[0]

        st.subheader("Ticket Information")

        st.write(
            "Employee ID:",
            selected_ticket["Employee_ID"]
        )

        st.write(
            "Category:",
            selected_ticket["Request_Category"]
        )

        st.write(
            "Description:",
            selected_ticket["Description"]
        )

        st.write(
            "Priority:",
            selected_ticket["Priority"]
        )

        st.write(
            "Current Status:",
            selected_ticket["Status"]
        )

        new_status = st.selectbox(
            "Update Ticket Status",
            ["Open", "In Progress", "Resolved"],
            index=[
                "Open",
                "In Progress",
                "Resolved"
            ].index(selected_ticket["Status"])
        )

        if st.button("Update Ticket"):

            updated_data = df.copy()

            ticket_index = updated_data.index[
                updated_data["Ticket_ID"] == ticket_id
            ][0]

            updated_data.loc[
                ticket_index, "Status"
            ] = new_status

            if new_status == "Resolved":

                resolution_time = pd.Timestamp.now()

                request_time = updated_data.loc[
                    ticket_index, "Request_Date"
                ]

                updated_data.loc[
                    ticket_index, "Resolution_Date"
                ] = resolution_time

                updated_data.loc[
                    ticket_index, "Resolution_Time_Hours"
                ] = round(
                    (
                        resolution_time - request_time
                    ).total_seconds() / 3600,
                    2
                )

            else:

                updated_data.loc[
                    ticket_index, "Resolution_Date"
                ] = pd.NaT

                updated_data.loc[
                    ticket_index, "Resolution_Time_Hours"
                ] = float("nan")

            save_data(updated_data)

            st.success("Ticket updated successfully!")

            st.rerun()

# --------------------------------------------------
# 9. VIEW AND FILTER ALL TICKETS
# --------------------------------------------------

elif page == "All Tickets":

    st.header("All IT Service Requests")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Open", "In Progress", "Resolved"]
    )

    category_filter = st.selectbox(
        "Filter by Category",
        ["All", "Hardware", "Software", "Network", "Access"]
    )

    filtered_data = df.copy()

    if status_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Status"] == status_filter
        ]

    if category_filter != "All":

        filtered_data = filtered_data[
            filtered_data["Request_Category"] == category_filter
        ]

    st.write(
        f"Records displayed: {len(filtered_data)}"
    )

    st.dataframe(
        filtered_data,
        use_container_width=True,
        hide_index=True
    )

    csv_download = filtered_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Requests",
        data=csv_download,
        file_name="filtered_it_requests.csv",
        mime="text/csv"
    )
