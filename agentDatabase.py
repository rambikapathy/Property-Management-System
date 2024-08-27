import sqlite3
import tkinter as tk
from tkinter import Text

# Create database if it doesn't exist
conn = sqlite3.connect('agents.db')
c = conn.cursor()

# Create table to store agent's login credentials 
c.execute('''CREATE TABLE IF NOT EXISTS agents (
                name TEXT,
                surname TEXT,
                branch TEXT,
                employee_id TEXT,
                username TEXT,
                password TEXT
            )''')
conn.commit()

def insertAgentData(name, surname, branch, employee_id, username, password):
    # Insert data into SQLite database named 'agent'
    c.execute("INSERT INTO agents (name, surname, branch, employee_id, username, password) VALUES (?, ?, ?, ?, ?, ?)",
              (name, surname, branch, employee_id, username, password))
    conn.commit()

def reviewAgentData(parent_window):
    viewWindow = tk.Toplevel(parent_window, bg="blue")
    viewWindow.title("Registered Agents")
    viewWindow.geometry("500x400")
    
    c.execute("SELECT * FROM agents")
    agents = c.fetchall()
    
    text = Text(viewWindow, bg="blue", fg="white", wrap="word")
    text.pack(expand=True, fill="both")
    
    for agent in agents:
        text.insert(tk.END, f"Name: {agent[0]}\nSurname: {agent[1]}\nBranch: {agent[2]}\nEmployee ID: {agent[3]}\nUsername: {agent[4]}\nPassword: {agent[5]}\n\n")
    text.config(state="disabled")

# Close the database connection when the script ends
import atexit
atexit.register(lambda: conn.close())
