import tkinter as tk
from tkinter import ttk
import sqlite3

def createConnection():
    """Initialize connection to the SQLite database."""
    return sqlite3.connect('properties.db')#make connection with property database, to keep track of changes to property and appointment table.

def validateLogTable():#create table for tracking system logs
    """Create the system_log table if it does not exist."""
    with createConnection() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS system_log (
            timestamp TEXT,
            username TEXT,
            employee_id INTEGER,
            action TEXT,
            details TEXT
        );
        """)
        conn.commit()

#check and update system log schema using PRAGMA queries.
def updateSystemLogScheme():
    """Check and update the schema of the system_log table."""
    with createConnection() as conn:
        c = conn.cursor()
        c.execute("PRAGMA table_info(system_log);")
        #execute pragma table to retreive metadata regards column from systemLog table
        #this function also executes SQLite statements to help acheive this.
        columns = [column[1] for column in c.fetchall()]
        #if any columns from the table are missing, the code executes the ALTER TABLE SQL command to add the missing column to the system_log table
        if 'username' not in columns:
            c.execute("ALTER TABLE system_log ADD COLUMN username TEXT;")
        if 'employee_id' not in columns:
            c.execute("ALTER TABLE system_log ADD COLUMN employee_id INTEGER;")
        if 'action' not in columns:
            c.execute("ALTER TABLE system_log ADD COLUMN action TEXT;")
        if 'details' not in columns:
            c.execute("ALTER TABLE system_log ADD COLUMN details TEXT;")

        conn.commit()

#this function optimsies a GUI window for storing and displaying active system monitoring
#the display of system logs are utilised through treeView.
def systemLogWindow(parent_window=None):
    """Create and display the System Log window."""
    logWindow = tk.Toplevel(parent_window) if parent_window else tk.Toplevel()
    logWindow.title("System Log")
    logWindow.geometry("1920x1080")  
    logWindow.configure(bg="beige")  

    tk.Label(logWindow, text="System Log", font=("Helvetica", 16), bg="beige", fg="brown").pack(pady=20)

    columns = ("Timestamp", "Username", "Action")#columns
    tree = ttk.Treeview(logWindow, columns=columns, show="headings")#treeview to output logs

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=300, anchor=tk.W)  

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


    vsb = ttk.Scrollbar(logWindow, orient="vertical", command=tree.yview)#scrollbar
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

#function loads log data from database table into the Treeview widget.
    def validateLogs():
        """Load log data from the database into the Treeview."""
        for item in tree.get_children():
            tree.delete(item)  #remove any pre-exisitng data in loops before loading new data

        with createConnection() as conn:
            c = conn.cursor()
            c.execute("SELECT timestamp, username, action FROM system_log ORDER BY timestamp DESC")
            rows = c.fetchall()
            for row in rows: #iteration for fetching queries
                row = tuple('rishi7668' if value is None else value for value in row)
                tree.insert("", tk.END, values=row)

    validateLogTable()  # Ensure the System log table exists
    updateSystemLogScheme()  # Ensure the table schema is correct
    validateLogs()  # validate active system logs

    tk.Button(logWindow, text="Refresh", command=validateLogs, bg="brown", fg="white").pack(pady=10)
    tk.Button(logWindow, text="Close Window", command=logWindow.destroy, bg="brown", fg="white").pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  


    mainWindow = tk.Toplevel()
    mainWindow.title("Main Menu")
    mainWindow.geometry("300x200")
    mainWindow.configure(bg="beige") 
    tk.Button(mainWindow, text="View System Log", command=lambda: systemLogWindow(mainWindow), bg="brown", fg="white").pack(pady=10)
    tk.Button(mainWindow, text="Close", command=mainWindow.destroy, bg="brown", fg="white").pack(pady=10)

    mainWindow.mainloop()
