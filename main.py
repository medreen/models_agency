from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_products,get_sales,insert_products,insert_sales,available_stock,get_stock,insert_stock,check_user_exists, insert_users
from flask_bcrypt import Bcrypt
from functools import wraps
import json
from database import * # Ensure all functions above are imported
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

#assigning an object to flask class
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  #

#creating a bcrypt object for password hashing
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        account_type = request.form['account_type']  # Get the account type from the form

        # Check if the user exists in the database
        user = check_user_exists(email)
        if user:
            flash('Account already exists.', 'warning')
        if not user and account_type == 'model':  # Ensure account type is valid
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            height_cm = request.form['height_cm']
            weight_kg = request.form['weight_kg']
            bust_cm = request.form['bust_cm']
            waist_cm = request.form['waist_cm']
            hips_cm = request.form['hips_cm']
            shoe_size = request.form['shoe_size']
            eye_color = request.form['eye_color']
            hair_color = request.form['hair_color']
            category = request.form['category']
            experience_yrs = request.form['experience_yrs']
            is_available = request.form['is_available']
            rate_per_hour = request.form['rate_per_hour']
            agency_id = request.form['agency_id']
            new_model = (phone, date_of_birth, gender, height_cm, weight_kg, bust_cm, waist_cm, hips_cm, shoe_size, eye_color, hair_color, category, experience_yrs, is_available, rate_per_hour, agency_id)

            # Insert the model into the database
            insert_model(new_model)  # Insert the model into the database
            flash('Account created successfully. Please log in.', 'success')
        elif not user and account_type == 'agency':  # Ensure account type is valid
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            website = request.form['website']
            city = request.form['city']
            country = request.form['country']
            agency_type = request.form['agency_type']
            founded_year = request.form['founded_year']
            commission_pct = request.form['commission_pct']
            new_agency = (name, email, phone, website, city, country, agency_type, founded_year, commission_pct)
            insert_agency(new_agency)
            flash('Account created successfully. Please log in.', 'success')

    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        
        user = check_user_exists(email)
        if user and bcrypt.check_password_hash(user['password'], password):  # Assuming password is stored in the 4th column        
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/models')
@login_required
def models_dashboard():
    job_listings = get_model_jobs(session['user_id'])  # Fetch jobs for the current model
    collaborations = get_model_collaborations(session['user_id'])  # Fetch collaborations for the current model
    agencies = get_model_agencies(session['user_id'])  # Fetch agencies for the current model
    return render_template('models.html', job_listings=job_listings, collaborations=collaborations, agencies=agencies)

@app.route('/jobs')
@login_required
def jobs():
    job_listings = get_all_jobs()  # Fetch all jobs from the database
    return render_template('jobs.html', job_listings=job_listings)

@app.route('/agency')
@login_required
def agency():
    agency_jobs = get_agency_jobs(session['user_id']) 
    collaborations = get_agency_collaborations(session['user_id'])  # Fetch collaborations for the current agency
    amodel_agency = get_model_agencies(session['user_id'])  # Fetch agencies for the current model
    return render_template('agency.html', agency_jobs=agency_jobs, collaborations=collaborations, model_agency=model_agency )

@app.route('/dashboard')
@login_required
def fetch_statistics():
    jobs_listings = get_all_jobs()  # Fetch all jobs from the database
    collaborations_listings = get_all_collaborations()  # Fetch all collaborations from the database
    collaboration_models = get_all_collaboration_models()  # Fetch all collaboration models from the database
    agency_listings = get_all_agencies()  # Fetch all agencies from the database
    model_listings = get_all_models()  # Fetch all models from the database
    return render_template('collaborations.html', collaboration_listings=collaboration_listings, collaboration_models=collaboration_models, agency_listings=agency_listings, model_listings=model_listings, jobs_listings=jobs_listings)

@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        agency_id = session['user_id']  # Assuming the logged-in user is the agency
        assigned_model_id = request.form['assigned_model_id']
        job_type = request.form['job_type']
        status = request.form['status']
        location = request.form['location']
        city = request.form['city']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        rate_per_hour = request.form['rate_per_hour']
        total_hours = request.form['total_hours']

        # Create a tuple with the job values
        new_job = (title, description, agency_id, assigned_model_id, job_type, status, location, city, start_date, end_date, rate_per_hour, total_hours)

        # Insert the job into the database
        insert_job(new_job)
        return redirect(url_for('jobs'))

    return render_template('dashboard.html')  # Render the job creation form

@app.route('/fetch_jobs')
@login_required
def fetch_agency_jobs():
    agency_jobs = get_agency_jobs(session['user_id'])
    return render_template('jobs.html', agency_jobs=agency_jobs)

@app.route('/fetch_collaborations')
@login_required
def fetch_agency_collaborations():
    collaborations = get_agency_collaborations(session['user_id'])
    return render_template('agency.html', collaborations=collaborations)

@app.route('/fetch_agencies')
@login_required
def fetch_model_agencies():
    model_agency = get_model_agencies(session['user_id'])
    return render_template('agency.html', model_agency=model_agency)

@app.route('/add_collaboration', methods=['GET', 'POST'])
@login_required
def add_collaboration():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        job_id = request.form['job_id']
        agency_id = session['user_id']  # Assuming the logged-in user is the agency
        collab_type = request.form['collab_type']
        status = request.form['status']
        partner_name = request.form['partner_name']
        partner_email = request.form['partner_email']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        deal_value = request.form['deal_value']
        commission_pct = request.form['commission_pct']

        # Create a tuple with the collaboration values
        new_collaboration = (title, description, job_id, agency_id, collab_type, status, partner_name, partner_email, start_date, end_date, deal_value, commission_pct)

        # Insert the collaboration into the database
        insert_collaboration(new_collaboration)
        return redirect(url_for('collaborations'))

    return render_template('dashboard.html') 
    
@app.route('/add_collaboration_model', methods=['GET', 'POST'])
@login_required
def add_collaboration_model():
    if request.method == 'POST':
        # Extract form data
        name = request.form['name']
        description = request.form['description']
        agency_id = session['user_id']  # Assuming the logged-in user is the agency
        model_type = request.form['model_type']
        status = request.form['status']
        experience_level = request.form['experience_level']
        rate_per_hour = request.form['rate_per_hour']

        # Create a tuple with the collaboration model values
        new_model = (name, description, agency_id, model_type, status, experience_level, rate_per_hour)

        # Insert the collaboration model into the database
        insert_collaboration_model(new_model)
        return redirect(url_for('collaboration_models'))

    return render_template('dashboard.html')  # Render the collaboration model creation form

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))