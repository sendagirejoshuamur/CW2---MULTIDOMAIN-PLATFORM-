**MULTI-DOMAIN INTELLIGENCE PLATFORM**

**Student Name:** Joshua Sendagire  
**Student ID:** M01045908  
**Project:** CST1510 - CW2 - Multi-Domain Intelligence Platform  

---

## Project Overview

A comprehensive, web-based multi-domain intelligence and incident management platform built with Streamlit. This application provides a unified dashboard for visualizing and analyzing cyber incidents, IT service tickets, and datasets across security and operational domains. The platform features secure authentication, interactive data exploration, and actionable insights through a modern, layered architecture.

---
Here's your **Login Credentials** section formatted properly for a README file:

---

## Login Credentials

### Default Admin Account
You can use the following pre-configured admin account to access the platform:

- **Username:** `Admin`
- **Password:** `Admin@123`

### Creating Additional Admin Accounts
To create additional admin accounts:
1. Register a new account with your desired username
2. **Select "Admin" as your role** during registration
3. **Logout and login again** to activate admin privileges  
   *Note: Admin features only become available after the first logout/login cycle*

### User Registration
The platform supports self-registration with two roles:
- **User**: Standard access to dashboards and data viewing
- **Admin**: Full system access including user management and administrative features

---

## Important Notes
- All passwords are securely hashed using bcrypt before storage
- User data is stored in `DATA/user_info.txt` (hashed credentials only)
- Session management ensures secure access across all pages
- Role-based permissions control access to different platform features

---

## Features

### **Security & Authentication**
- Secure user authentication with session management
- Role-based access control and protected routes
- Secure credential handling via Streamlit secrets

### **Multi-Domain Intelligence Dashboard**
- **Cyber Incidents Dashboard**: Track, filter, and visualize security incidents by category, severity, and status
- **IT Tickets Management**: Monitor service desk tickets with status tracking and analysis
- **Datasets Catalog**: Browse and search available intelligence datasets with metadata
- **AI Analysis Module**: Advanced analytics and pattern detection capabilities
- **Admin Dashboard**: Access administrative features with dedicated admin role

### **Data Visualization & Interaction**
- Interactive charts and metrics for real-time data exploration
- Dynamic filtering by date, category, severity, and status
- Search functionality across incident descriptions and metadata
- Sidebar controls with responsive data filtering

### **Data Management**
- CSV file upload and processing capabilities
- Database persistence with SQLite integration
- CRUD operations for incidents, tickets, and user data
- File-based and database storage options

### **Administrative Features**
- User management interface
- insert, update, and delete for dashboards
- Delete data from dashboards and database
- clear database tables

---

## Technical Architecture

### **Three-Layer Architecture**

1. **Data Layer** (`app/data/`)
   - Database connections and SQLite operations
   - CSV data loaders and file processors
   - Schema definitions and data models
   - Dedicated modules for incidents, tickets, datasets, and users

2. **Services Layer** (`app/services/`)
   - Business logic and data processing
   - File upload handling and validation
   - User management and authentication services
   - Intelligence analysis algorithms

3. **Presentation Layer** (`pages/`, `main.py`)
   - Streamlit multi-page application interface
   - Dashboard visualizations and UI components
   - User navigation and page routing
   - Authentication interface and login flow

### **Project Structure**
```
CW2_MULTI_DOMAIN_PLATFORM/
├── streamlit/secrets.toml          # Configuration and secrets
├── app/data/                       # Data access layer
├── app/services/                   # Business logic layer
├── DATA/                           # Static datasets
├── pages/                          # Streamlit application pages
├── uploaded_files/                 # User upload storage
├── auth.py                         # ignore this
├── login.py                        # Login interface and application entrypoint
└── main.py                         # ignore this
```

### **Security Implementation**
- Password hashing with bcrypt and automatic salting
- Session-based authentication with secure state management
- Input validation and sanitization for all user inputs
- Protected data access with proper authorization checks
- Secure file handling and upload validation

### **Data Storage**
- **Primary Database**: SQLite (`intelligence_platform.db`)
- **File Storage**: CSV files for datasets and exports
- **User Data**: Secure text file(user_info.txt) storage with hashed credentials
- **Session State**: Streamlit session management for user state

---

## User Experience

The platform offers an intuitive, guided workflow:
1. **Secure Login**: Role-based authentication with credential validation
2. **Dashboard Navigation**: Clear menu system for accessing different intelligence domains
3. **Interactive Exploration**: Filter, search, and visualize data in real-time
4. **Insight Generation**: Automated analysis and actionable recommendations
5. **Data Management**: Upload and process. 

The interface maintains consistency across modules with sidebar controls, main content displays, and responsive layouts that adapt to different data types and user needs.

---

## Technical Specifications

- **Framework**: Streamlit 1.28+
- **Database**: SQLite3 with SQLAlchemy-style operations
- **Security**: bcrypt for password hashing, session-based auth
- **Data Processing**: Pandas for data manipulation and analysis
- **Visualization**: Streamlit charts and metrics
- **File Handling**: CSV, with support for additional formats
- **Architecture**: Modular, layered design with separation of concerns

---

## Installation & Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```



2. **Launch application**:
   ```bash
   streamlit run login.py
   ```

---



## Future Enhancements

- Real-time data streaming and alerts
- Integration with external threat intelligence feeds
- Mobile-responsive design and progressive web app features
- Advanced reporting and automated documentation

---

*This platform represents a professional-grade intelligence solution that bridges multiple operational domains, providing security teams and IT professionals with the tools needed for effective incident management and data-driven decision making.*