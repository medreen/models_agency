import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

try:
    conn = psycopg2.connect(database=os.getenv("DB_NAME"),
                            user=os.getenv("DB_USER"),
                            password=os.getenv("DB_PASS"),
                            host=os.getenv("DB_HOST"),
                            port=os.getenv("DB_PORT"))
    print("Database connected successfully")
except Exception as e: 
    print(f"Database not connected successfully: {e}")
cur = conn.cursor(cursor_factory=RealDictCursor)

def insert_model(values):
    try:
        cur.execute('''
            INSERT INTO models (
                first_name, last_name, email, phone, password,
                date_of_birth, gender, height_cm, weight_kg,
                bust_cm, waist_cm, hips_cm, shoe_size,
                eye_color, hair_color, category, is_available,
                experience_yrs,  rate_per_hour, portfolio_url, profile_photo_url, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            ) RETURNING id
        ''', values)
        conn.commit()
        return cur.fetchone()['id']
        print("Model inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting model: {e}")

def insert_agency(values):
    try:
        cur.execute('''
            INSERT INTO agency (
                name, email, phone, password, website, address, city, country, agency_type, founded_year, commission_pct, logo_url, instagram_url, created_at, updated_at,
                total_models
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s

            ) RETURNING id
        ''', values)
        conn.commit()
        return cur.fetchone()['id']
        print("Agency inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting agency: {e}")

def insert_job(values):
    try:
        cur.execute('''
            INSERT INTO jobs (
                title, description, agency_id, assigned_model_id,
                job_type, status, location, city, country,
                start_date, end_date, start_time, end_time, rate_per_hour, total_hours, currency, is_paid, gender_required, min_height_cm, max_height_cm, category_required, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''', values)
        conn.commit()
        print("Job inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting job: {e}")

def insert_collaboration(values):
    try:
        cur.execute('''
            INSERT INTO collaborations (
                title, description, job_id, agency_id,
                collab_type, status, partner_name, partner_phone, partner_email, partner_website, currency,
                start_date, end_date, deal_value, commission_pct, commission_amount, is_paid, contract_url, is_signed, signed_at, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''', values)
        conn.commit()
        print("Collaboration inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting collaboration: {e}")

def insert_collaboration_model(values):
    try:
        cur.execute('''
            INSERT INTO collaboration_models (
                collaboration_id, model_id, role, fee
            ) VALUES (
                %s, %s, %s, %s
            )
        ''', values)
        conn.commit()
        print("Collaboration model inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting collaboration model: {e}")
        r

def get_all_models():
    try:
        cur.execute('SELECT * FROM models')
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching models: {e}")
        return []

def get_model_agencies(model_id):
    try:
        cur.execute('SELECT * FROM agency WHERE model_id = %s', (assigned_model_id,))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching agencies: {e}")
        return []

def get_model_jobs(assigned_model_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE assigned_model_id = %s', (assigned_model_id,))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching jobs: {e}")
        return []

def get_pending_jobs(assigned_model_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE assigned_model_id = %s AND status = %s', (assigned_model_id, 'pending'))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching pending jobs: {e}")
        return []
        
def get_model_collaborations(model_id):
    try:
        cur.execute('SELECT * FROM collaborations WHERE model_id = %s', (model_id,))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching collaborations: {e}")        
        return []

def get_all_agencies():
    try:
        cur.execute('SELECT * FROM agency')
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching agencies: {e}")
        return []

def get_agency_jobs(agency_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE agency_id = %s', (agency_id,))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching jobs: {e}")
        return []

def get_agency_collaborations(agency_id):
    try:
        cur.execute('SELECT * FROM collaborations WHERE agency_id = %s', (agency_id,))
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching collaborations: {e}")
        return []

def get_all_jobs():
    try:
        cur.execute('SELECT * FROM jobs')
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching jobs: {e}")        
        return []

def get_all_collaborations():
    try:
        cur.execute('SELECT * FROM collaborations')
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching collaborations: {e}")
        return []

def get_all_collaboration_models():
    try:
        cur.execute('SELECT * FROM collaboration_models')
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching collaboration models: {e}")
        return []

def get_model_by_email(email):
    try:
        cur.execute('SELECT * FROM models WHERE email = %s', (email,))
        return cur.fetchone()
    except Exception as e:
        conn.rollback()
        print(f"Error fetching model by email: {e}")
        return []

def check_model_exists(email):
    try:
        cur.execute('SELECT * FROM models WHERE email = %s', (email,))
        return cur.fetchone() 
    except Exception as e:
        conn.rollback()
        print(f"Error checking if model exists: {e}")
        return []

def check_agency_exists(email):
    try:
        cur.execute('SELECT * FROM agency WHERE email = %s', (email,))
        return cur.fetchone()
    except Exception as e:
        conn.rollback()
        print(f"Error checking if agency exists: {e}")
        return []
        

def update_job_status_on_acceptance(job_id: int, model_response: str):
    """
    Updates a job's status based on the model's response.
    model_response should be 'accepted', 'declined', or 'pending'.
    """
    valid_statuses = ('accepted', 'declined', 'pending')

    if model_response not in valid_statuses:
        raise ValueError(f"Invalid model_response: {model_response}")

    try:
        cur.execute(
            """
            UPDATE jobs
            SET status = %s
            WHERE id = %s
            RETURNING id, status;
            """,
            (model_response, job_id),
        )
        updated_row = cur.fetchone()
        conn.commit()

        if updated_row is None:
            raise ValueError(f"No job found with id {job_id}")

        return updated_row
    except Exception as e:
        conn.rollback()
        print(f"Error updating status: {e}")
        return None

        
def get_active_jobs(agency_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE agency_id = %s AND status = %s', (agency_id, 'confirmed'))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching closed jobs: {e}")
        return []