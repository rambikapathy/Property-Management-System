import sqlite3

def create_connection():
    """Create a database connection to the SQLite database."""
    return sqlite3.connect('properties.db')

def create_tables():
    """Create the necessary tables."""
    conn = create_connection()
    cursor = conn.cursor()

    # iniiate properties table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE NOT NULL,
            asking_price REAL NOT NULL,
            bedrooms INTEGER NOT NULL,
                   
            category TEXT NOT NULL,
            market_date TEXT NOT NULL,
            vendor TEXT NOT NULL,
            photo_path TEXT,
            video_path TEXT
        );
    ''')

    # implemented appointments table, that stores appointment details.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            property_address TEXT NOT NULL,  -- Changed from property_id to property_address
            time TEXT NOT NULL,
            viewer_name TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            email_address TEXT NOT NULL,
            notes TEXT
        );
    ''')

    conn.commit()
    conn.close()

#function to store new appoitnments into appointment table
def initiateAppointment(date, property_address, time, viewer_name, contact_number, email_address, notes):
    """Insert a new appointment into the appointments table."""
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO appointments (date, property_address, time, viewer_name, contact_number, email_address, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, property_address, time, viewer_name, contact_number, email_address, notes))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while inserting appointment: {e}")
        return False
    finally:
        conn.close()

#function to filter appointments based on date/time, property address etc.
def filterAppointments(date=None, property_address=None, time=None):
    """Fetch appointments from the appointments table."""
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM appointments WHERE 1=1"
    params = []

    if date:
        query += " AND date = ?"#filter appointment by date
        params.append(date)
    
    if property_address:
        query += " AND property_address = ?"#filter appointment by property
        params.append(property_address)
    
    if time:
        query += " AND time = ?"#filter appointment by time
        params.append(time)

    cursor.execute(query, params)
    appointments = cursor.fetchall()
    conn.close()

    return appointments

def deleteAppointment(appointment_id):
    """Delete an appointment from the appointments table."""
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while deleting appointment: {e}")
        return False
    finally:
        conn.close()

def update_appointment(appointment_id, date, property_address, time, viewer_name, contact_number, email_address, notes):
    """Update an existing appointment in the appointments table."""
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE appointments
            SET date = ?, property_address = ?, time = ?, viewer_name = ?, contact_number = ?, email_address = ?, notes = ?
            WHERE id = ?
        ''', (date, property_address, time, viewer_name, contact_number, email_address, notes, appointment_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred while updating appointment: {e}")
        return False
    finally:
        conn.close()
