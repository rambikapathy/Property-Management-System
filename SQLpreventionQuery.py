import sqlite3
import bcrypt #library to hash password during agent registration and login.

# Connect with agent database
def connect_db():
    return sqlite3.connect('agents.db')

# Allow agent to register their details for creating login credentials.
def addAgentInfo(name, surname, branch, employee_id, username, password):
    """Insert agent registration into the database."""
    hashPassword = enteredPassword(password)
    query = '''INSERT INTO agents (name, surname, branch, employee_id, username, password)
               VALUES (?, ?, ?, ?, ?, ?)'''
    with connect_db() as conn:
        c = conn.cursor()
        try:
            #Entered credential values are passed separately in a tuple when implementing 'execute'
            c.execute(query, (name, surname, branch, employee_id, username, hashPassword))
            conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                #Block any duplicate registrations with same employee ID or username
                print("Error: Employee ID or Username already exists.")
            else:
                print(f"Error: {e}")

# Retreive agent login credentials from agent database
def retreiveData():
    """Retrieve all agents from the database."""
    #Query to prevent SQL injection attacks
    #This query retrievies data, use placeholders to prevent SQL injection attacks. 
    query = "SELECT * FROM agents"
    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query)
        return c.fetchall()

# Hash the password that is entered by agent whilst typing
def enteredPassword(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Check if hash password matches with stored password in agent database
def validatePassword(savedPassword, providePassword):
    """Check if hash password matches with stored password in agent database"""
    return bcrypt.checkpw(providePassword.encode('utf-8'), savedPassword)

