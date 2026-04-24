# Employee Management System (EMS)

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white) ![Python](https://img.shields.io/badge/python-v3.12-yellow) ![SQLite](https://img.shields.io/badge/sqlite-blue)

**Employee Management System (EMS)** is a web-based administrative portal developed as an internship project for **CSPDCL** (Chhattisgarh State Power Distribution Company Limited) in 2025. The system streamlines organizational workflows by providing role-based access for Admins, Managers, and Employees.

##  Features

* **Role-Based Access Control**: Secure login portals tailored for Admin, Manager, and Employee roles.
* **Employee Management**: Admins can add, update, and manage employee profiles and organizational data.
* **Leave Request System**: Employees can submit leave requests, which Managers can track and process.
* **Profile Management**: Employees can view and manage their individual professional details.
* **Dashboards**: Dedicated views for Admins and Managers to monitor system activity and personnel data.

##  Tech Stack

* **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
* **Database**: [SQLite](https://www.sqlite.org/)
* **Authentication**: [Flask-Login](https://flask-login.readthedocs.io/)
* **Templating**: Jinja2 (HTML/CSS)

##  Getting Started

Follow these steps to run the project locally.

### Prerequisites

* Python (v3.12 or higher)
* pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd EmployeeManagementSystem
    ```

2.  **Set up the Virtual Environment**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install flask flask-login
    ```

4.  **Run the Application**
    ```bash
    python app.py
    ```

5.  **Access the App**
    Open your browser and navigate to `http://127.0.0.1:5000`.

##  Team Members

* **Shashank Pradhan**
* **Kiran Vishwakarma**
* **Aarekh Verma**
* **S Satvika**

---
*Developed as an internship project for CSPDCL (2025).*
