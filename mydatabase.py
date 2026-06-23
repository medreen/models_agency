import psycopg2

DB_NAME = "agent_models"
DB_USER = "postgres"
DB_PASS = "Colesprouse2311!"
DB_HOST = "localhost"
DB_PORT = "5432" 
try:
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print("Database connected successfully")
except Exception as e: 
    print(f"Database not connected successfully: {e}")

cur = conn.cursor()

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

def get_all_agencies():
    try:
        cur.execute('SELECT * FROM agency')
        return cur.fetchall()
    except Exception as e:
        print(f"Error fetching agencies: {e}")

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



