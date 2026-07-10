from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from mydatabase import get_model_by_email, update_job_status_on_acceptance, get_closed_jobs, get_pending_jobs, insert_model, insert_agency, check_agency_exists, check_model_exists, get_all_jobs, get_all_collaborations, get_all_collaboration_models, get_all_agencies, get_all_models, insert_job, insert_collaboration, insert_collaboration_model, get_model_jobs, get_model_collaborations, get_model_agencies, get_agency_jobs, get_agency_collaborations
from datetime import datetime
from flask_bcrypt import Bcrypt
import os
from werkzeug.security import generate_password_hash, check_password_hash
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
        if 'email' not in session:
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
        phone = request.form['phone']
        password = request.form['password']
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
        is_available = request.form['is_available'] == 'true'
        experience_yrs = request.form['experience_yrs']
        rate_per_hour = request.form['rate_per_hour']
        portfolio_url = request.form['portfolio_url']
        profile_photo_url = request.form['profile_photo_url']
        updated_at = datetime.now()
        created_at = datetime.now()
       
        model = check_model_exists(email)
        if not model:
            hashed_password = generate_password_hash(password)
            new_model = (
                first_name, last_name, email, phone, hashed_password,
                date_of_birth, gender, height_cm, weight_kg,
                bust_cm, waist_cm, hips_cm, shoe_size,
                eye_color, hair_color, category, is_available,
                experience_yrs, rate_per_hour, portfolio_url,
                profile_photo_url, created_at, updated_at
            )
            insert_model(new_model)
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Account already exists.', 'warning')
    return render_template('registermodel.html')

   
@app.route('/register_agency', methods=['GET', 'POST'])
def register_agency():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        website = request.form['website']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        agency_type = request.form['agency_type']
        founded_year = request.form['founded_year']
        commission_pct = request.form['commission_pct']
        logo_url = request.form['logo_url']
        instagram_url = request.form['instagram_url']
        total_models = request.form['total_models']
        updated_at = datetime.now()
        created_at = datetime.now()

        agent = check_agency_exists(email)
        if not agent:
            hashed_password = generate_password_hash(password)
            new_agency = (
                name, email, phone, hashed_password, website,
                address, city, country, agency_type, founded_year,
                commission_pct,               
                logo_url, instagram_url, created_at, updated_at, total_models
            )
            insert_agency(new_agency)
            return redirect(url_for('login'))
            flash('Account created successfully. Please log in.', 'success')
        else:
            flash('Account already exists.', 'warning')
    return render_template('registerAgency.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        agency_exists = check_agency_exists(email)
        model_exists = check_model_exists(email)
        if model_exists and check_password_hash(model_exists.get('password'), password):  # Assuming password is stored in the 4th column        
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        elif agency_exists and check_password_hash(agency_exists.get('password'), password):  # Assuming password is stored in the 4th column
            flash('Login successful.', 'success')
            return redirect(url_for('jobs'))  # Redirect to dashboard after successful login
            
        else:
            return redirect(url_for('register_model'))
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')  # Render the login form

@app.route('/models')
# @login_required
def models_dashboard():
    job_listings = get_model_jobs(session.get('model_id'))  # Fetch jobs for the current model
    collaborations = get_model_collaborations(session.get('model_id'))  # Fetch collaborations for the current model
    agencies = get_model_agencies(session.get('model_id'))  # Fetch agencies for the current model
    return render_template('models.html', job_listings=job_listings, collaborations=collaborations, agencies=agencies)


@app.route('/add_job', methods=['GET', 'POST'])
# @login_required
def add_job():  
    if request.method == 'POST':
        # Extract form data
        title = request.form['title']        
        agency_id = session.get('agency_id')  # Assuming the logged-in user is the agency
        assigned_model_id = request.form['assigned_model_id']
        job_type = request.form['job_type']        
        location = request.form['location']
        city = request.form['city']
        country = request.form['country']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        rate_per_hour = request.form['rate_per_hour']               
        currency = request.form['currency']
        status = request.form['status']
        is_paid = request.form['is_paid']
        gender_required = request.form['gender_required']
        category_required = request.form['category_required']
        min_height_cm = request.form.get('min_height-cm')
        max_height_cm = request.form.get('max_height_cm')        
        description = request.form['description']
        created_at = datetime.now()
        updated_at = datetime.now()

        # Create a tuple with the job values
        new_job = (title, agency_id, assigned_model_id, job_type, location, city, country, start_date, end_date, start_time, end_time, rate_per_hour,  currency, status, is_paid, gender_required, category_required, min_height_cm, max_height_cm,  description, created_at, updated_at)

        # Insert the job into the database
        insert_job(new_job)
        return redirect(url_for('jobs'))

    return render_template('dashboard.html')  


@jobs_bp.route("/jobs/<int:job_id>/respond", methods=["POST"])
def respond_to_job(job_id):
    model_id = session.get("model_id")  # however you're tracking the logged-in model
    if not model_id:
        flash("Log in as model to respond to job requests.")
        return redirect(url_for("login"))

    response = request.form.get("response")  # "accepted" or "declined"
    if response not in ("accepted", "declined"):
        flash("Invalid response.")
        return redirect(url_for("models_dashboard"))

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

@app.route('/jobs')
# @login_required
def jobs():
    is_agent = session.get('agency_id')
    is_model = session.get('model_id')

    agency_jobs = get_agency_jobs(is_agent)
    model_job_invites = get_pending_jobs(is_model)
    closed_jobs = get_closed_jobs(is_model)
    job_listings = get_all_jobs()

    return render_template(
        'jobs.html',
        agency_jobs=agency_jobs,
        model_job_invites=model_job_invites,
        closed_jobs=closed_jobs,
        job_listings=job_listings,
        is_agent=is_agent,
        is_model=is_model
    )

@app.route('/agency')
# @login_required
def agency(): 
    agencies = get_all_agencies
    collaborations = get_all_collaborations
    return render_template('agency.html', agencies=agencies, collaborations=collaborations)

@app.route('/dashboard')
# @login_required
def fetch_statistics():
    jobs_listings = get_all_jobs()  # Fetch all jobs from the database
    collaborations_listings = get_all_collaborations()  # Fetch all collaborations from the database
    collaboration_models = get_all_collaboration_models()  # Fetch all collaboration models from the database
    agency_listings = get_all_agencies()  # Fetch all agencies from the database
    models = get_all_models()  # Fetch all models from the database
    return render_template('dashboard.html', collaborations_listings=collaborations_listings, collaboration_models=collaboration_models, agency_listings=agency_listings, models=models, jobs_listings=jobs_listings)

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