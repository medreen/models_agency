from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from mydatabase import get_model_by_email, insert_model, insert_agency, check_agency_exists, check_model_exists, get_all_jobs, get_all_collaborations, get_all_collaboration_models, get_all_agencies, get_all_models, insert_job, insert_collaboration, insert_collaboration_model, get_model_jobs, get_model_collaborations, get_model_agencies, get_agency_jobs, get_agency_collaborations
from datetime import datetime
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

#assigning an object to flask class
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  #

jobs_bp = Blueprint("jobs", __name__)

#creating a bcrypt object for password hashing
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'model_id' not in session or 'agency_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register_model', methods=['GET', 'POST'])
def register_model():
    if request.method == 'POST':      
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
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
        portfolio_url = request.form['portfolio_url']
        profile_photo_url = request.form['profile_photo_url']
        created_at = datetime.now()
        updated_at = datetime.now()  

        email_exists = check_model_exists(email)
        if email_exists:        
            flash('Account already exists.', 'warning')
            return redirect(url_for('login'))
        else:
            new_model = (first_name, last_name, email, password, phone, date_of_birth, gender, height_cm, weight_kg, bust_cm, waist_cm, hips_cm, shoe_size, eye_color, hair_color, category, experience_yrs, is_available, rate_per_hour, portfolio_url, profile_photo_url, created_at, updated_at)

            # Insert the model into the database
            insert_model(new_model)  # Insert the model into the database
            flash('Account created successfully. Please log in.', 'success')
           
    return render_template('registermodel.html')

@app.route('/register_agency', methods=['GET', 'POST'])
def register_agency():
    if request.method == 'POST':
        email = request.form['email']
        agent = check_agency_exists(email)

        if not agent:  # Ensure account type is valid
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            website = request.form['website']
            city = request.form['city']
            country = request.form['country']
            agency_type = request.form['agency_type']
            founded_year = request.form['founded_year']
            commission_pct = request.form['commission_pct']
            new_agency = (name, email, phone, website, city, country, agency_type, founded_year, commission_pct)
            insert_agency(new_agency)
            flash('Account created successfully. Please log in.', 'success')
        elif agent:
            flash('Account already exists.', 'warning')
    return render_template('registerAgency.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        agency = check_agency_exists(session.get('agency_id'), email)
        models = check_model_exists(email)
        if models and bcrypt.check_password_hash(models['password'], password):  # Assuming password is stored in the 4th column        
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        elif agency and bcrypt.check_password_hash(agency['password'], password):  # Assuming password is stored in the 4th column
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
            
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')  # Render the login form

@app.route('/models')
# @login_required
def models_dashboard():
    job_listings = get_model_jobs(session['model_id'])  # Fetch jobs for the current model
    collaborations = get_model_collaborations(session['model_id'])  # Fetch collaborations for the current model
    agencies = get_model_agencies(session['model_id'])  # Fetch agencies for the current model
    return render_template('models.html', job_listings=job_listings, collaborations=collaborations, agencies=agencies)

@app.route('/jobs')
# @login_required
def jobs():
    job_listings = get_all_jobs()  # Fetch all jobs from the database
    return render_template('jobs.html', job_listings=job_listings)

@app.route('/agency')
# @login_required
def agency():
    agency_jobs = get_agency_jobs(session['agency_id']) 
    collaborations = get_agency_collaborations(session['agency_id'])  # Fetch collaborations for the current agency
    model_agency = get_model_agencies(session['model_id'])  # Fetch agencies for the current model
    return render_template('agency.html', agency_jobs=agency_jobs, collaborations=collaborations, model_agency=model_agency )

@app.route('/dashboard')
# @login_required
def fetch_statistics():
    jobs_listings = get_all_jobs()  # Fetch all jobs from the database
    collaborations_listings = get_all_collaborations()  # Fetch all collaborations from the database
    collaboration_models = get_all_collaboration_models()  # Fetch all collaboration models from the database
    agency_listings = get_all_agencies()  # Fetch all agencies from the database
    model_listings = get_all_models()  # Fetch all models from the database
    return render_template('collaborations.html', collaboration_listings=collaboration_listings, collaboration_models=collaboration_models, agency_listings=agency_listings, model_listings=model_listings, jobs_listings=jobs_listings)

@app.route('/add_job', methods=['GET', 'POST'])
# @login_required
def add_job():
    verified_agent = session.get(agency_id)
    if not verified_agent:
        flash('Access denied for this action', 'warning')

    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        agency_id = session['agency_id']  # Assuming the logged-in user is the agency
        assigned_model_id = request.form['assigned_model_id']
        job_type = request.form['job_type']
        status = request.form['status']
        location = request.form['location']
        city = request.form['city']
        country = request.form['country']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        rate_per_hour = request.form['rate_per_hour']
        total_hours = request.form['total_hours']
        total_pay = request.form['total_pay']
        currency = request.form['currency']
        is_paid = request.form['is_paid']
        gender_required = request.form['gender_required']
        min_height_cm = request.form['min_height_cm']
        max_height_cm = request.form['max_height_cm']
        category_required = request.form['category_required']
        created_at = datetime.now()
        updated_at = datetime.now()

        # Create a tuple with the job values
        new_job = (title, description, agency_id, assigned_model_id, job_type, status, location, city, country, start_date, end_date, start_time, end_time, rate_per_hour, total_hours, total_pay, currency, is_paid, gender_required, min_height_cm, max_height_cm, category_required, created_at, updated_at)

        # Insert the job into the database
        insert_job(new_job)
        return redirect(url_for('jobs'))

    return render_template('dashboard.html')  


@jobs_bp.route("/jobs/<int:job_id>/respond", methods=["POST"])
def respond_to_job(job_id):
    model_id = session.get("model_id")  # however you're tracking the logged-in model
    if not model_id:
        flash("Please log in to respond to job requests.")
        return redirect(url_for("login"))

    response = request.form.get("response")  # "accepted" or "declined"
    if response not in ("accepted", "declined"):
        flash("Invalid response.")
        return redirect(url_for("models.dashboard"))

    try:
        update_job_status_on_acceptance(
            job_id=job_id,
            model_id=model_id,
            model_response=response,
        )
        flash(f"Job {response} successfully.")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("models_dashboard"))

@app.route('/fetch_jobs')
# @login_required
def fetch_agency_jobs():
    agency_jobs = get_agency_jobs(session['agency_id'])
    return render_template('jobs.html', agency_jobs=agency_jobs)

@app.route('/fetch_collaborations')
# @login_required
def fetch_agency_collaborations():
    collaborations = get_agency_collaborations(session['agency_id'])
    return render_template('agency.html', collaborations=collaborations)

@app.route('/fetch_agencies')
# @login_required
def fetch_model_agencies():
    model_agency = get_model_agencies(session['model_id'])
    return render_template('agency.html', model_agency=model_agency)

@app.route('/add_collaboration', methods=['GET', 'POST'])
# @login_required
def add_collaboration():
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']
        description = request.form['description']
        job_id = request.form['job_id']
        agency_id = session['agency_id']  # Assuming the logged-in user is the agency
        collab_type = request.form['collab_type']
        status = request.form['status']
        partner_name = request.form['partner_name']
        partner_email = request.form['partner_email']
        partner_website = request.form['partner_website']
        partner_phone = request.form['partner_phone']
        start_date = request.form['start_date']
        end_date = request.form['end_date']        
        is_paid = request.form['is_paid']
        deal_value = request.form['deal_value']
        commission_pct = request.form['commission_pct']
        commission_amount = request.form['commision_amount']
        currency = request.form['currency']
        contract_url = request.form['contract_url']
        is_signed = request.form['is_signed']
        signed_at = request.form['signed_at']
        created_at = request.form['created_at']
        updated_at = request.form['updated_at']

        # Create a tuple with the collaboration values
        new_collaboration = (title, description, job_id, agency_id, collab_type, status, partner_name, partner_phone, partner_email, partner_website, start_date, end_date, deal_value, commission_pct, commission_amount, is_paid, contract_url, is_signed, signed_at, created_at, updated_at)

        # Insert the collaboration into the database
        insert_collaboration(new_collaboration)
        return redirect(url_for('collaborations'))

    return render_template('dashboard.html') 
    
@app.route('/collaboration_models')
# @login_required
def collaboration_models():
    if request.method == 'POST':
        collaboration_id = request.form['collaboration_id']
        if collaboration_id == session['collaboration_id']:
            model_id = request.form['model_id']
            role = request.form['role']
            fee = request.form['fee']
            new_collaboration_model = (collaboration_id, model_id, role, fee)
            insert_collaboration_model(new_collaboration_model)

            return redirect(url_for('collaboration_models'))
    return render_template('models.html')  # Render the collaboration models page

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

app.run(debug=True)