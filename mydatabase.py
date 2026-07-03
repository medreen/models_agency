import psycopg2
import os
from dotenv import load_dotenv

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

cur = conn.cursor()

def insert_users(values):
    try:
        cur.execute('''
            INSERT INTO users (username, email, password, account_type)
            VALUES (%s, %s, %s, %s)
        ''', values)
        conn.commit()
        print("User inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting user: {e}")

def insert_model(values):
    try:
        cur.execute('''
            INSERT INTO models (
                first_name, last_name, email, phone,
                date_of_birth, gender, height_cm, weight_kg,
                bust_cm, waist_cm, hips_cm, shoe_size,
                eye_color, hair_color, category,
                experience_yrs, is_available, rate_per_hour, agency_id
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s
            )
        ''', values)
        conn.commit()
        print("Model inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting model: {e}")

def insert_agency(values):
    try:
        cur.execute('''
            INSERT INTO agency (
                name, email, phone, website,
                city, country, agency_type,
                founded_year, commission_pct
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s
            )
        ''', values)
        conn.commit()
        print("Agency inserted successfully")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting agency: {e}")

def insert_job(values):
    try:
        cur.execute('''
            INSERT INTO jobs (
                title, description, agency_id, assigned_model_id,
                job_type, status, location, city,
                start_date, end_date, rate_per_hour, total_hours
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
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
                collab_type, status, partner_name, partner_email,
                start_date, end_date, deal_value, commission_pct
            ) VALUES (
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
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

def get_all_models():
    try:
        cur.execute('SELECT * FROM models')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching models: {e}")

def get_model_agencies(model_id):
    try:
        cur.execute('SELECT * FROM agency WHERE model_id = %s', (model_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching agencies: {e}")

def get_model_jobs(model_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE model_id = %s', (model_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching jobs: {e}")

def get_model_collaborations(model_id):
    try:
        cur.execute('SELECT * FROM collaborations WHERE model_id = %s', (model_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching collaborations: {e}")

def get_all_agencies():
    try:
        cur.execute('SELECT * FROM agency')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching agencies: {e}")

def get_agency_jobs(agency_id):
    try:
        cur.execute('SELECT * FROM jobs WHERE agency_id = %s', (agency_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching jobs: {e}")

def get_agency_collaborations(agency_id):
    try:
        cur.execute('SELECT * FROM collaborations WHERE agency_id = %s', (agency_id,))
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching collaborations: {e}")

def get_all_jobs():
    try:
        cur.execute('SELECT * FROM jobs')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching jobs: {e}")

def get_all_collaborations():
    try:
        cur.execute('SELECT * FROM collaborations')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching collaborations: {e}")

def get_all_collaboration_models():
    try:
        cur.execute('SELECT * FROM collaboration_models')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching collaboration models: {e}")



