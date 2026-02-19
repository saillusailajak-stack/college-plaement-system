from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# File path
DATA_FILE = 'data/placement_targets.csv'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Create CSV file with headers if it doesn't exist
def init_csv():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'department', 'company', 'role', 'status'])

init_csv()

# Home route - redirect to login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple hardcoded login (you can change this)
        if username == 'admin' and password == 'admin123':
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# Dashboard - show all students
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    students = []
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            students = list(reader)
    except:
        students = []
    
    # Calculate statistics
    total = len(students)
    placed = sum(1 for s in students if s.get('status', '') == 'Placed')
    pending = total - placed
    
    return render_template('dashboard.html', 
                         students=students, 
                         total=total, 
                         placed=placed, 
                         pending=pending)

# Add new student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_student = {
            'id': request.form['id'],
            'name': request.form['name'],
            'department': request.form['department'],
            'company': request.form['company'],
            'role': request.form['role'],
            'status': request.form['status']
        }
        
        # Append to CSV
        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'name', 'department', 'company', 'role', 'status'])
            writer.writerow(new_student)
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_student.html')

# Delete student
@app.route('/delete/<student_id>')
def delete_student(student_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    students = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        students = list(reader)
    
    # Remove the student with matching id
    students = [s for s in students if s['id'] != student_id]
    
    # Write back to file
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'department', 'company', 'role', 'status'])
        writer.writeheader()
        writer.writerows(students)
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# Update student status
@app.route('/update/<student_id>', methods=['POST'])
def update_status(student_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    new_status = request.form['status']
    
    students = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        students = list(reader)
    
    # Update the status
    for student in students:
        if student['id'] == student_id:
            student['status'] = new_status
            break
    
    # Write back to file
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'name', 'department', 'company', 'role', 'status'])
        writer.writeheader()
        writer.writerows(students)
    
    flash('Status updated successfully!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
