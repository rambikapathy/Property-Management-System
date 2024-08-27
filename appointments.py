import sqlite3

def create_connection():
    """Create and return a database connection."""
    try:
        #Establish connection with appointment database
        conn = sqlite3.connect('appointments.db')
        return conn
    except sqlite3.Error as e: # print errors f there are issues when connecting to database.
        print(f"Database Error: {e}")
        return None


def filterAppointments(date=None, property_id=None, time=None):
    """Fetch appointments from the database."""
    conn = create_connection()
    if not conn:
        return []
    #Optimise query to select all columns from 'appointment' table
    query = "SELECT * FROM appointments"
    #Store any particular query conditions along with its associated parameters.
    conditions = []
    parameters = []
    
    #This part of the code filters queries, if argument to functions are provided.
    if date:
        conditions.append("date = ?")#filter queries relating to date
        parameters.append(date)
    if property_id:
        conditions.append("property_id = ?")#filter queries relating to property
        parameters.append(property_id)
    if time:
        conditions.append("time = ?")#filter queries relating to time
        parameters.append(time)
    
    if conditions:#if conditions exist, necessiate the query with WHERE AND commands
        query += " WHERE " + " AND ".join(conditions)
    
    #Implement cursor object during the execution of queries.
    try:
        cursor = conn.cursor()
        #Execute SQL query with its corresponding parameters
        cursor.execute(query, parameters)
        #fetch all relevant rows that match in accordance with the query
        appointments = cursor.fetchall()
    except sqlite3.Error as e:
        #Prints any forseen errors during query execution
        print(f"Database Error: {e}")
        appointments = []# throw error message, if the list is empty 
    finally:
        conn.close()
    
    return appointments# this outputs all the saved appointments list.

#Function to add new set of client appointments to the database under a new row.
def initiateAppointment(date, property_id, time, viewer_name, contact_number, email_address, notes):
    """Insert a new appointment into the database.""" #SQL insert statement
    conn = create_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (date, property_id, time, viewer_name, contact_number, email_address, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (date, property_id, time, viewer_name, contact_number, email_address, notes)
        )
        conn.commit()#save appointment changes to database.
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

#Delete appointment function
def deleteAppointment(appointment_id):
    """Delete an appointment from the database."""
    conn = create_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()
