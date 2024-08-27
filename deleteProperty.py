import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

#Connection to property database.
def createConnection():
    """Initialize connection to the SQLite database."""
    return sqlite3.connect('properties.db')

#If table for storing system logs does not exist, then create one.
def createLogTable():
    """Create a table for logging system actions."""
    conn = createConnection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS system_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user TEXT NOT NULL,
                    action TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()


#If agent deletes property listings, this will automatically be stored in the active system log table in the property database
def log_action(user, action):
    """Log actions in the system_log table."""
    conn = createConnection()
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO system_log (timestamp, user, action) VALUES (?, ?, ?)",
              (timestamp, user, action))
    conn.commit()
    conn.close()

def deletePropertyWindow():
    """Create and display the Delete Property window."""
    # Ensure the log table is active to record properties being deleted.
    createLogTable()  

    deleteProperty = tk.Toplevel(bg="beige")  
    deleteProperty.title("Delete Property")
    deleteProperty.geometry("400x300")
    deleteProperty.resizable(False, False)

    tk.Label(deleteProperty, text="Delete Property", bg="beige", fg="black").pack(pady=20)  

#Delete property listing by getting agent to input valid property ID.
    tk.Label(deleteProperty, text="Property ID:", bg="beige", fg="black").pack(pady=5)  
    propertyIdInput = tk.Entry(deleteProperty)
    propertyIdInput.pack(pady=5)

#Properties from the property database will be retreived, prior to deletion.
    def submitDeletion():
        conn = createConnection()
        c = conn.cursor()
        property_id = int(propertyIdInput.get())
        
        c.execute("SELECT address FROM properties WHERE id=?", (property_id,))
        address = c.fetchone()
        
        if not address:#If property ID does not exists or already has been deleted, throw error message.
            messagebox.showerror("Deletion Error", "Property ID not found.")
            conn.close()
            return
        
        address = address[0]
        c.execute("DELETE FROM properties WHERE id=?", (property_id,))
        conn.commit()
        
        log_action('User1', f'Deleted property with ID: {property_id}, Address: {address}')  # Replace 'User1' with actual username
        #If valid property ID is provided, delete property lisitng.
        messagebox.showinfo("Delete Property", "Property deleted successfully!")
        deleteProperty.destroy()
        conn.close()

    button_options = {'bg': 'brown', 'fg': 'white'}  

    tk.Button(deleteProperty, text="Submit", command=submitDeletion, **button_options).pack(pady=10)
    tk.Button(deleteProperty, text="Close Window", command=deleteProperty.destroy, **button_options).pack(pady=10)

if __name__ == '__main__':
    createLogTable()  # Ensure the log table is created

