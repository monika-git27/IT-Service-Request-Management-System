
# IT Service Request Management System

**Python | Streamlit | Pandas | Microsoft Excel | Power Query**

## Project Overview

Developed an IT Service Request Management System to digitalize employee IT support requests, automate ticket management, and improve visibility into IT service operations.

The project integrates a Python-based Streamlit application with an interactive Microsoft Excel dashboard, enabling request submission, automated ticket assignment, status tracking, and operational performance reporting.

The application maintains ticket records in a CSV file, which serves as the data source for an Excel dashboard connected through Power Query.

## Business Problem

Manual IT support request management can create several operational challenges:

- Difficulty tracking requests across different departments.
- Manual effort involved in recording and assigning support tickets.
- Limited visibility into unresolved and overdue requests.
- Inconsistent tracking of ticket resolution times.
- Time-consuming preparation of IT service performance reports.

This project addresses these challenges through a centralized request management prototype and an integrated reporting dashboard.

## Project Objectives

- Digitalize employee IT support request submission.
- Automate ticket ID generation and support team assignment.
- Enable tracking of ticket priority, category, and resolution status.
- Identify overdue requests using predefined demonstration thresholds.
- Develop an interactive Excel dashboard to monitor IT service performance.
- Integrate application data with Excel reporting through Power Query.

## Tools & Technologies

| Technology | Purpose |
|---|---|
| Python | Application logic and workflow automation |
| Streamlit | Interactive request management interface |
| Pandas | Data processing and ticket record management |
| CSV | Ticket data storage |
| Microsoft Excel | KPI dashboard, PivotTables, PivotCharts, and slicers |
| Power Query | Data connection and refresh between CSV and Excel |
| VS Code | Application development |

## Key Features

### 1. IT Request Submission

Developed a Streamlit interface allowing employees to submit IT support requests.

The application captures:

- Employee ID and department
- Request category
- Issue description
- Request priority
- Submission date

Mandatory field validation prevents incomplete requests from being submitted.

### 2. Automated Ticket Management

Implemented Python-based automation to:

- Generate unique ticket IDs.
- Assign requests to the appropriate IT support team based on issue category.
- Set the initial ticket status to Open.
- Store new requests in the CSV dataset.
- Record ticket status updates.
- Calculate resolution time when requests are resolved.

The system supports three ticket statuses: **Open, In Progress, and Resolved**.

### 3. Ticket Tracking and Monitoring

Developed functionality to view and manage existing support tickets.

Users can:

- Review ticket details.
- Update ticket statuses.
- Filter requests by category and status.
- Identify overdue unresolved tickets.
- Export filtered ticket records.

Overdue tickets are identified using illustrative priority-based resolution thresholds configured for the prototype.

### 4. Interactive Excel Dashboard

Built an Excel dashboard to monitor IT support operations using KPI cards, PivotTables, PivotCharts, and slicers.

**Key Performance Indicators**

- Total Tickets
- Open Tickets
- In Progress Tickets
- Resolved Tickets
- Overdue Tickets
- Average Resolution Time

**Dashboard Visualizations**

- Ticket Status Distribution
- Tickets by Priority
- Tickets by Category
- Tickets by Department
- Monthly Ticket Trends

Interactive slicers enable filtering and exploration of ticket data across different categories, priorities, departments, and statuses.

### 5. Streamlit and Excel Integration

Integrated the Streamlit application with Microsoft Excel reporting through a shared CSV data source.

**Data Workflow**

1. Employees submit requests or IT staff update ticket statuses in Streamlit.
2. Python processes the changes and updates the CSV file.
3. Excel Power Query connects to the CSV file.
4. Refreshing the Excel connection updates the imported records and related PivotTables.
5. The dashboard reflects the latest available ticket information.

This approach separates operational request management from analytical reporting while maintaining a consistent underlying data source.

## Dataset

The project uses a fictional IT service request dataset containing 400 initial records.

The dataset includes the following fields:

| Field | Description |
|---|---|
| Ticket_ID | Unique ticket identifier |
| Request_Date | Request submission timestamp |
| Employee_ID | Employee identifier |
| Department | Employee department |
| Request_Category | Hardware, Software, Network, or Access |
| Description | Description of the reported issue |
| Priority | Low, Medium, or High |
| Assigned_Team | Responsible IT support team |
| Status | Current ticket status |
| Resolution_Date | Ticket resolution timestamp |
| Resolution_Time_Hours | Time taken to resolve the request |

New requests submitted through the application are added to the existing dataset.

**Data Source:** Synthetic data generated for educational and portfolio demonstration purposes. No real employee or organizational information is used.


## Business Value

The solution demonstrates how a lightweight digital application can improve routine IT service management activities.

**Operational Efficiency:** Automates repetitive ticket creation, categorization, and assignment tasks.

**Process Standardization:** Establishes a consistent structure for recording and tracking IT support requests.

**Improved Visibility:** Provides centralized access to ticket statuses, priorities, and overdue requests.

**Data-Driven Reporting:** Enables IT support performance monitoring through an interactive Excel dashboard.

**Simplified Reporting Workflow:** Connects operational data with Excel analytics, reducing the need for repeated manual data imports.



## Conclusion

The IT Service Request Management System demonstrates the practical application of Python automation, lightweight application development, and Excel-based business reporting.

By combining a Streamlit request management interface with an integrated Excel dashboard, the project illustrates how routine IT support processes can be digitalized, standardized, and monitored through a simple technology solution.

**Core Skills Demonstrated:** Python Automation, Business Process Digitalization, Streamlit Application Development, Data Management, Excel Dashboard Development, Power Query Integration, KPI Reporting, and Data Validation.
