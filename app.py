from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import time

app = Flask(__name__)
app.secret_key = "hackersecretrecipe"  # Change this to a strong secret key in production

# Simulated database (in-memory)
users = {}
projects = {}  

lock = threading.Lock() 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash("Username already exists!", "error")
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        projects[username] = []  # Initialize user's project list
        flash("Signup successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users or not check_password_hash(users[username], password):
            flash("Invalid username or password!", "error")
            return redirect(url_for('login'))

        session['username'] = username
        flash("Login successful!", "success")
        return redirect(url_for('dashboard'))

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    username = session['username']
    user_projects = projects.get(username, [])

    if request.method == 'POST':
        if 'project_name' in request.form:  # Creating a new project
            project_name = request.form['project_name']

            if len(user_projects) >= 1:  
                flash("Free users can create only one project!", "error")
                return redirect(url_for('dashboard'))

            time.sleep(1)

            user_projects.append(project_name)
            projects[username] = user_projects
            flash(f"Project '{project_name}' created successfully!", "success")

        elif 'delete_project' in request.form:  # Deleting a project
            project_name = request.form['delete_project']
            if project_name in user_projects:
                user_projects.remove(project_name)
                projects[username] = user_projects
                flash(f"Project '{project_name}' deleted successfully!", "success")

    return render_template('dashboard.html', username=username, projects=user_projects)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
