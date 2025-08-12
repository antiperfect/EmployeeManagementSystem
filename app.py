from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Flask Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'employee_login'

# Flask Login
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# Load User from DB
@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# Login Validation
def validate_user(username, password, role):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, role FROM users WHERE username = ? AND role = ?", (username, role))
    row = cur.fetchone()
    conn.close()
    if row and check_password_hash(row[2], password):
        return User(row[0], row[1], row[3])
    return None

# Database initialization function 
def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    
    # Create users table with all required fields
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Personal Information
            title TEXT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            gender TEXT,
            dob TEXT,
            category TEXT,
            contact_number TEXT,
            email_address TEXT,
            blood_group TEXT,
            is_disabled INTEGER DEFAULT 0,
            disability_type TEXT,
            employee_number TEXT UNIQUE,
            
            -- Account Information
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'employee',
            manager_id INTEGER,
            
            -- Education Information - 12th
            has_12th INTEGER DEFAULT 0,
            `12th_stream` TEXT,
            `12th_percentage` REAL,
            `12th_year` TEXT,
            `12th_school` TEXT,
            `12th_board` TEXT,
            
            -- Education Information - Graduation
            has_graduation INTEGER DEFAULT 0,
            graduation_degree TEXT,
            graduation_specialization TEXT,
            graduation_cgpa REAL,
            graduation_college TEXT,
            graduation_year TEXT,
            
            -- Education Information - Post Graduation
            has_pg INTEGER DEFAULT 0,
            pg_degree TEXT,
            pg_specialization TEXT,
            pg_cgpa REAL,
            pg_college TEXT,
            pg_year TEXT,
            
            -- Education Information - PhD
            has_phd INTEGER DEFAULT 0,
            phd_field TEXT,
            phd_specialization TEXT,
            phd_status TEXT,
            phd_university TEXT,
            phd_year TEXT,
            phd_thesis TEXT,
            
            -- Allotment Information
            office TEXT,
            designation TEXT,
            employee_type TEXT,
            subgroup TEXT,
            `class` TEXT,
            
            -- Foreign Key Constraint
            FOREIGN KEY (manager_id) REFERENCES users (id)
        )
    """)
    print("Created users table")
    
    # Create leave_records table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS leave_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            remaining_medical_leave INTEGER,
            remaining_optional_leave INTEGER,
            remaining_casual_leave INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    print("Created leave_records table")
    
    # Create indexes for better performance
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_employee_number ON users(employee_number)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_manager_id ON users(manager_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leave_records_user_id ON leave_records(user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_leave_records_status ON leave_records(status)")
    print("Created indexes")
    
    # Check if default admin exists
    cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    if cur.fetchone()[0] == 0:
        # Insert default admin user
        admin_password = generate_password_hash('admin123')
        cur.execute("""
            INSERT INTO users (
                title, first_name, last_name, gender, dob, category,
                contact_number, email_address, blood_group, employee_number,
                username, password, role,
                office, designation, employee_type, subgroup, `class`
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Mr.', 'Admin', 'User', 'Male', '1980-01-01', 'General',
            '9999999999', 'admin@company.com', 'O+', 'EMP000001',
            'admin', admin_password, 'admin',
            'Raipur Gudhiyari', 'Administrator', 'Regular', 'Admin', '1'
        ))
        print("Created default admin user")
    
    # Check if default manager exists
    cur.execute("SELECT COUNT(*) FROM users WHERE username = 'manager'")
    if cur.fetchone()[0] == 0:
        # Insert default manager user
        manager_password = generate_password_hash('manager123')
        cur.execute("""
            INSERT INTO users (
                title, first_name, last_name, gender, dob, category,
                contact_number, email_address, blood_group, employee_number,
                username, password, role,
                office, designation, employee_type, subgroup, `class`
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'Ms.', 'Manager', 'User', 'Female', '1985-01-01', 'General',
            '8888888888', 'manager@company.com', 'A+', 'EMP000002',
            'manager', manager_password, 'manager',
            'Raipur Gudhiyari', 'Manager', 'Regular', 'Management', '2'
        ))
        print("Created default manager user")
    
    conn.commit()
    conn.close()
    print("Database initialization completed!")
    print("Default admin login: username='admin', password='admin123'")
    print("Default manager login: username='manager', password='manager123'")

# Routes from new app.py (unchanged)
@app.route('/')
def home():
    return redirect(url_for('homepage'))

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'], 'admin')
        if user:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials')
    return render_template('admin_login.html')

@app.route('/manager-login', methods=['GET', 'POST'])
def manager_login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'], 'manager')
        if user:
            login_user(user)
            return redirect(url_for('manager_dashboard'))
        flash('Invalid manager credentials')
    return render_template('manager_login.html')

@app.route('/employee-login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'], 'employee')
        if user:
            login_user(user)
            return redirect(url_for('employee_dashboard'))
        flash('Invalid employee credentials')
    return render_template('employee_login.html')

@app.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Unauthorized access", 403
    return render_template('admin_dashboard.html', current_user=current_user)

@app.route('/manager-dashboard')
@login_required
def manager_dashboard():
    if current_user.role != 'manager':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Get the office of the manager
    cur.execute("SELECT office FROM users WHERE id = ?", (current_user.id,))
    office_row = cur.fetchone()

    if not office_row or not office_row[0]:
        flash("⚠️ Office not assigned to this manager.")
        return redirect(url_for('logout'))

    manager_office = office_row[0]

    # Get employees from same office
    cur.execute("""
        SELECT id, first_name, last_name, employee_number, designation, email_address
        FROM users
        WHERE role = 'employee' AND office = ?
        ORDER BY first_name
    """, (manager_office,))
    employees = cur.fetchall()

    # Get leave requests from same office
    cur.execute("""
        SELECT lr.id, u.first_name || ' ' || u.last_name, u.employee_number,
               lr.leave_type, lr.start_date, lr.end_date, lr.reason, lr.status
        FROM leave_records lr
        JOIN users u ON u.id = lr.user_id
        WHERE u.office = ?
        ORDER BY lr.start_date DESC
    """, (manager_office,))
    
    leave_requests = [
        {
            'id': row[0],
            'name': row[1],
            'emp_id': row[2],
            'type': row[3],
            'start': row[4],
            'end': row[5],
            'reason': row[6],
            'status': row[7]
        }
        for row in cur.fetchall()
    ]

    conn.close()

    return render_template('manager_dashboard.html',
                           manager_name=current_user.username,
                           employees=employees,
                           leave_requests=leave_requests)

@app.route('/employee-dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Get current employee's info including their office
    cur.execute("""
        SELECT first_name, last_name, dob, gender, category, employee_number, office
        FROM users WHERE id = ?
    """, (current_user.id,))
    emp = cur.fetchone()

    if not emp:
        conn.close()
        flash("Employee record not found.")
        return redirect(url_for('logout'))

    employee_info = {
        'first_name': emp[0],
        'last_name': emp[1],
        'dob': emp[2],
        'gender': emp[3],
        'category': emp[4],
        'employee_number': emp[5],
    }

    employee_office = emp[6]

    # ✅ Fetch manager working in the same office
    cur.execute("""
        SELECT first_name, last_name
        FROM users
        WHERE role = 'manager' AND office = ?
        LIMIT 1
    """, (employee_office,))
    mgr = cur.fetchone()

    manager_name = f"{mgr[0]} {mgr[1]}" if mgr else "Not Assigned"

    # Fetch leave history
    cur.execute("""
        SELECT leave_type, start_date, end_date, status
        FROM leave_records
        WHERE user_id = ?
        ORDER BY start_date DESC
    """, (current_user.id,))
    leave_history = [
        {'type': r[0], 'start': r[1], 'end': r[2], 'status': r[3]}
        for r in cur.fetchall()
    ]

    conn.close()

    return render_template('employee_dashboard.html',
                           employee=employee_info,
                           manager_name=manager_name,
                           leave_history=leave_history)




@app.route('/leave-request', methods=['GET', 'POST'])
@login_required
def leave_request():
    if current_user.role != 'employee':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    if request.method == 'POST':
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        reason = request.form['reason']

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_requested = (end - start).days + 1

        cur.execute("""
            SELECT leave_type, SUM(
                julianday(end_date) - julianday(start_date) + 1
            )
            FROM leave_records
            WHERE user_id = ? AND status = 'Approved'
            GROUP BY leave_type
        """, (current_user.id,))
        leaves_used = dict(cur.fetchall() or [])

        leave_limits = {'medical': 20, 'optional': 3, 'casual': 13}
        remaining = {
            lt: leave_limits[lt] - int(leaves_used.get(lt, 0))
            for lt in leave_limits
        }

        if days_requested > remaining.get(leave_type, 0):
            flash(f"❌ Not enough {leave_type} leaves remaining.")
            conn.close()
            return redirect(url_for('leave_request'))

        cur.execute("""
            INSERT INTO leave_records (
                user_id, leave_type, start_date, end_date, reason,
                remaining_medical_leave, remaining_optional_leave, remaining_casual_leave
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            current_user.id, leave_type, start_date, end_date, reason,
            remaining['medical'], remaining['optional'], remaining['casual']
        ))

        conn.commit()
        conn.close()
        flash("✅ Leave request submitted successfully.")  # This will now show on dashboard
        return redirect(url_for('leave_request'))  # ✅ CHANGED LINE

    conn.close()
    return render_template('leave_request.html')


@app.route('/my-profile', methods=['GET'])
@login_required
def my_profile():
    if current_user.role != 'employee':
        return "Unauthorized", 403
        
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT title, first_name, last_name, gender, dob, category, contact_number,
               email_address, blood_group, is_disabled, disability_type, employee_number,
               has_12th, `12th_stream`, `12th_percentage`, `12th_year`, `12th_school`, `12th_board`,
               has_graduation, graduation_degree, graduation_specialization, graduation_cgpa,
               graduation_college, graduation_year,
               has_pg, pg_degree, pg_specialization, pg_cgpa, pg_college, pg_year,
               has_phd, phd_field, phd_specialization, phd_status, phd_university, phd_year, phd_thesis,
               office, designation, employee_type, subgroup, class
        FROM users WHERE id = ?
    """, (current_user.id,))
    user_data = cur.fetchone()
    conn.close()

    if not user_data:
        flash("Employee information not found.")
        return redirect(url_for('logout'))

    # Map the data to a more readable dictionary
    employee_info = {
        'personal': {
            'title': user_data[0],
            'first_name': user_data[1],
            'last_name': user_data[2],
            'gender': user_data[3],
            'dob': user_data[4],
            'category': user_data[5],
            'contact_number': user_data[6],
            'email_address': user_data[7],
            'blood_group': user_data[8],
            'is_disabled': bool(user_data[9]),
            'disability_type': user_data[10],
            'employee_number': user_data[11]
        },
        'education_12th': {
            'has_12th': bool(user_data[12]),
            'stream': user_data[13],
            'percentage': user_data[14],
            'year': user_data[15],
            'school': user_data[16],
            'board': user_data[17]
        },
        'graduation': {
            'has_graduation': bool(user_data[18]),
            'degree': user_data[19],
            'specialization': user_data[20],
            'cgpa': user_data[21],
            'college': user_data[22],
            'year': user_data[23]
        },
        'post_graduation': {
            'has_pg': bool(user_data[24]),
            'degree': user_data[25],
            'specialization': user_data[26],
            'cgpa': user_data[27],
            'college': user_data[28],
            'year': user_data[29]
        },
        'phd': {
            'has_phd': bool(user_data[30]),
            'field': user_data[31],
            'specialization': user_data[32],
            'status': user_data[33],
            'university': user_data[34],
            'year': user_data[35],
            'thesis': user_data[36]
        },
        'allotment': {
            'office': user_data[37],
            'designation': user_data[38],
            'employee_type': user_data[39],
            'subgroup': user_data[40],
            'class': user_data[41]
        }
    }

    return render_template('my_profile.html', employee=employee_info)

import re

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    if current_user.role != 'employee':
        return "Unauthorized", 403

    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE id = ?", (current_user.id,))
    user_row = cur.fetchone()

    if not user_row or not check_password_hash(user_row[0], current_password):
        flash("❌ Current password is incorrect.", "error")
        conn.close()
        return redirect(url_for('my_profile'))

    if new_password != confirm_password:
        flash("❌ New password and confirm password do not match.", "error")
        conn.close()
        return redirect(url_for('my_profile'))

    # Validate password complexity
    if (
        not re.search(r"[A-Z]", new_password) or
        not re.search(r"[0-9]", new_password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password)
    ):
        flash("❌ Password must contain at least 1 uppercase letter, 1 number, and 1 special character.", "error")
        conn.close()
        return redirect(url_for('my_profile'))

    hashed_password = generate_password_hash(new_password)
    cur.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, current_user.id))
    conn.commit()
    conn.close()

    flash("✅ Password changed successfully.", "success")
    return redirect(url_for('my_profile'))


# Enhanced add_employee route with allotment info
@app.route('/add-employee', methods=['GET', 'POST'])
@login_required
def add_employee():
    if current_user.role != 'admin':
        return "Unauthorized access", 403

    if request.method == 'POST':
        # Extract all form data
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        dob = request.form['dob']
        category = request.form['category']
        contact_number = request.form['contact_number']
        email_address = request.form['email_address']
        blood_group = request.form['blood_group']
        is_disabled = 1 if 'is_disabled' in request.form else 0
        disability_type = request.form.get('disability_type', '')
        employee_number = request.form['employee_number']
        username = request.form['username']
        password = request.form['password']
        manager_id = request.form.get('manager_id')
        
        # Allotment info
        office = request.form['office']
        designation = request.form['designation']
        employee_type = request.form['employee_type']
        subgroup = request.form['subgroup']
        emp_class = request.form['class']
        
        # Education fields
        has_12th = 1 if 'has_12th' in request.form else 0
        twelfth_stream = request.form.get('12th_stream', '')
        twelfth_percentage = request.form.get('12th_percentage', 0)
        twelfth_year = request.form.get('12th_year', '')
        twelfth_school = request.form.get('12th_school', '')
        twelfth_board = request.form.get('12th_board', '')
        
        has_graduation = 1 if 'has_graduation' in request.form else 0
        graduation_degree = request.form.get('graduation_degree', '')
        graduation_specialization = request.form.get('graduation_specialization', '')
        graduation_cgpa = request.form.get('graduation_cgpa', 0)
        graduation_college = request.form.get('graduation_college', '')
        graduation_year = request.form.get('graduation_year', '')
        
        has_pg = 1 if 'has_pg' in request.form else 0
        pg_degree = request.form.get('pg_degree', '')
        pg_specialization = request.form.get('pg_specialization', '')
        pg_cgpa = request.form.get('pg_cgpa', 0)
        pg_college = request.form.get('pg_college', '')
        pg_year = request.form.get('pg_year', '')
        
        has_phd = 1 if 'has_phd' in request.form else 0
        phd_field = request.form.get('phd_field', '')
        phd_specialization = request.form.get('phd_specialization', '')
        phd_status = request.form.get('phd_status', '')
        phd_university = request.form.get('phd_university', '')
        phd_year = request.form.get('phd_year', '')
        phd_thesis = request.form.get('phd_thesis', '')

        if manager_id == '':
            manager_id = None

        hashed_pw = generate_password_hash(password)

        try:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            
            # Fixed SQL query with proper escaping of 'class' column and correct parameter count
            cur.execute("""
                INSERT INTO users (
                    title, first_name, last_name, gender, dob, category,
                    contact_number, email_address, blood_group, is_disabled,
                    disability_type, employee_number, username, password, 
                    role, manager_id,
                    has_12th, `12th_stream`, `12th_percentage`, `12th_year`, `12th_school`, `12th_board`,
                    has_graduation, graduation_degree, graduation_specialization, graduation_cgpa,
                    graduation_college, graduation_year,
                    has_pg, pg_degree, pg_specialization, pg_cgpa, pg_college, pg_year,
                    has_phd, phd_field, phd_specialization, phd_status, phd_university, phd_year, phd_thesis,
                    office, designation, employee_type, subgroup, `class`
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title, first_name, last_name, gender, dob, category,
                contact_number, email_address, blood_group, is_disabled,
                disability_type, employee_number, username, hashed_pw,
                'employee', manager_id,
                has_12th, twelfth_stream, twelfth_percentage, twelfth_year, twelfth_school, twelfth_board,
                has_graduation, graduation_degree, graduation_specialization, graduation_cgpa,
                graduation_college, graduation_year,
                has_pg, pg_degree, pg_specialization, pg_cgpa, pg_college, pg_year,
                has_phd, phd_field, phd_specialization, phd_status, phd_university, phd_year, phd_thesis,
                office, designation, employee_type, subgroup, emp_class
            ))
            
            conn.commit()
            conn.close()
            flash(f"Employee '{first_name} {last_name}' (ID: {employee_number}) added successfully!")
            return redirect(url_for('add_employee'))
            
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                flash("❌ Username already exists. Try a different one.")
            elif 'employee_number' in str(e):
                flash("❌ Employee number already exists. Please refresh and try again.")
            else:
                flash(f"❌ Error adding employee: {str(e)}")
            return redirect(url_for('add_employee'))
        except Exception as e:
            flash(f"❌ Database error: {str(e)}")
            return redirect(url_for('add_employee'))

    return render_template('add_employee.html')

# Rest of the routes from new app.py (unchanged)
@app.route('/manage-employees')
@login_required
def manage_employees():
    if current_user.role != 'admin':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Fetch all employee details
    cur.execute("""
        SELECT id, title, first_name, last_name, gender, dob, category,
               employee_number, username, manager_id, office, designation,
               employee_type, subgroup, class
        FROM users
        WHERE role = 'employee'
        ORDER BY first_name, last_name
    """)
    employees = cur.fetchall()
    conn.close()

    return render_template('manage_employees.html', employees=employees)


@app.route('/view-employee/<int:employee_id>')
@login_required
def view_employee(employee_id):
    if current_user.role not in ['admin', 'manager']:
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, first_name, last_name, gender, dob, category, 
               employee_number, username, manager_id, office, designation, 
               employee_type, subgroup, class
        FROM users WHERE id = ? AND role = 'employee'
    """, (employee_id,))
    employee = cur.fetchone()
    conn.close()

    if not employee:
        flash("Employee not found")
        return redirect(url_for('manage_employees'))

    return render_template('view_employee.html', employee=employee)

@app.route('/edit-employee/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(employee_id):
    if current_user.role != 'admin':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        dob = request.form['dob']
        category = request.form['category']
        username = request.form['username']
        manager_id = request.form.get('manager_id')
        office = request.form['office']
        designation = request.form['designation']
        employee_type = request.form['employee_type']
        subgroup = request.form['subgroup']
        emp_class = request.form['class']
        
        if manager_id == '':
            manager_id = None

        try:
            cur.execute("""
                UPDATE users SET 
                    title = ?, first_name = ?, last_name = ?, gender = ?, 
                    dob = ?, category = ?, username = ?, manager_id = ?,
                    office = ?, designation = ?, employee_type = ?, subgroup = ?, class = ?
                WHERE id = ? AND role = 'employee'
            """, (title, first_name, last_name, gender, dob, category, 
                  username, manager_id, office, designation, employee_type, 
                  subgroup, emp_class, employee_id))
            
            conn.commit()
            conn.close()
            flash(f"Employee '{first_name} {last_name}' updated successfully!")
            return redirect(url_for('manage_employees'))
            
        except sqlite3.IntegrityError:
            flash("❌ Username already exists. Try a different one.")
            conn.close()
            return redirect(url_for('edit_employee', employee_id=employee_id))

    # GET request - fetch employee data
    cur.execute("""
        SELECT id, title, first_name, last_name, gender, dob, category, 
               employee_number, username, manager_id, office, designation, 
               employee_type, subgroup, class
        FROM users WHERE id = ? AND role = 'employee'
    """, (employee_id,))
    employee = cur.fetchone()
    conn.close()

    if not employee:
        flash("Employee not found")
        return redirect(url_for('manage_employees'))

    return render_template('edit_employee.html', employee=employee)

@app.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    
    # Get employee name before deletion for flash message
    cur.execute("SELECT first_name, last_name FROM users WHERE id = ? AND role = 'employee'", (user_id,))
    employee = cur.fetchone()
    
    if employee:
        cur.execute("DELETE FROM users WHERE id = ? AND role = 'employee'", (user_id,))
        conn.commit()
        flash(f"Employee '{employee[0]} {employee[1]}' deleted successfully.")
    else:
        flash("Employee not found.")
    
    conn.close()
    return redirect(url_for('manage_employees'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('employee_login'))

if __name__ == '__main__':
    # Initialize database (only creates leave_records table now)
    init_db()
    app.run(debug=True)

#manager management
import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('users.db')
cur = conn.cursor()

offices = ['Raipur Gudhiyari', 'Bilaspur', 'Durg', 'Jagdalpur', 'Ambikapur',]

# Insert managers
for i, office in enumerate(offices):
    username = f"manager_{i+1}"
    password = generate_password_hash("manager123")
    cur.execute("""
        INSERT INTO users (title, first_name, last_name, gender, dob, category,
                           employee_number, username, password, role)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'manager')
    """, ("Mr.", f"Manager{i+1}", office, "Male", "1985-01-01", "Power Distribution",
          f"M{i+1:03}", username, password))

# Get manager IDs
cur.execute("SELECT id FROM users WHERE role='manager'")
manager_ids = [row[0] for row in cur.fetchall()]

# Insert 4 employees under each manager
for m_id in manager_ids:
    for j in range(4):
        fname = f"Emp{m_id}_{j+1}"
        emp_num = f"E{m_id}{j+1:02}"
        uname = f"user_{m_id}_{j+1}"
        pwd = generate_password_hash("employee123")
        cur.execute("""
            INSERT INTO users (title, first_name, last_name, gender, dob, category,
                               employee_number, username, password, role, manager_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'employee', ?)
        """, ("Ms.", fname, "CSPDCL", "Female", "1995-05-01", "Line Staff",
              emp_num, uname, pwd, m_id))

conn.commit()
conn.close()

@app.route('/manager-dashboard')
@login_required
def manager_dashboard():
    if current_user.role != 'manager':
        return "Unauthorized", 403

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    # Step 1: Get the office of the current manager
    cur.execute("SELECT office FROM users WHERE id = ?", (current_user.id,))
    office_row = cur.fetchone()
    
    if not office_row or not office_row[0]:
        flash("⚠️ Office not assigned to manager.")
        return redirect(url_for('logout'))

    manager_office = office_row[0]

    # Step 2: Fetch employees from the same office
    cur.execute("""
        SELECT id, first_name, last_name, employee_number, designation, email_address
        FROM users
        WHERE role = 'employee' AND office = ?
        ORDER BY first_name
    """, (manager_office,))
    employees = cur.fetchall()

    # Step 3: Fetch leave requests from the same office
    cur.execute("""
        SELECT lr.id, u.first_name || ' ' || u.last_name, u.employee_number,
               lr.leave_type, lr.start_date, lr.end_date, lr.reason, lr.status
        FROM leave_records lr
        JOIN users u ON u.id = lr.user_id
        WHERE u.office = ?
        ORDER BY lr.start_date DESC
    """, (manager_office,))
    
    leave_requests = [
        {
            'id': row[0],
            'name': row[1],
            'emp_id': row[2],
            'type': row[3],
            'start': row[4],
            'end': row[5],
            'reason': row[6],
            'status': row[7]
        }
        for row in cur.fetchall()
    ]

    conn.close()

    return render_template('manager_dashboard.html',
                           manager_name=current_user.username,
                           employees=employees,
                           leave_requests=leave_requests)


@app.route('/approve-leave', methods=['POST'])
@login_required
def approve_leave():
    if current_user.role != 'manager':
        return "Unauthorized", 403

    leave_id = request.form.get('leave_id')

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE leave_records SET status = 'Approved' WHERE id = ?", (leave_id,))
    conn.commit()
    conn.close()

    flash("✅ Leave approved successfully.")
    return redirect(url_for('manager_dashboard'))

@app.route('/reject-leave', methods=['POST'])
@login_required
def reject_leave():
    if current_user.role != 'manager':
        return "Unauthorized", 403

    leave_id = request.form.get('leave_id')

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE leave_records SET status = 'Rejected' WHERE id = ?", (leave_id,))
    conn.commit()
    conn.close()

    flash("❌ Leave rejected.")
    return redirect(url_for('manager_dashboard'))

