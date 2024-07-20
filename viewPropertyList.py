import tkinter as tk
from databaseUtils import createConnection

def viewPropertyListWindow():
    viewWindow = tk.Toplevel(bg="black")
    viewWindow.title("View Properties")
    viewWindow.geometry("800x400")
    viewWindow.resizable(False, False)

    tk.Label(viewWindow, text="Properties List", bg="black", fg="white").pack(pady=20)

    propertiesList = tk.Listbox(viewWindow, bg="white", fg="black", width=100, height=15)
    propertiesList.pack(pady=10, fill=tk.BOTH, expand=True)

    conn = createConnection()
    c = conn.cursor()
    # Retrieve property listing from the 'properties' database
    c.execute("SELECT * FROM properties")
    properties = c.fetchall()
    
    # Add column headers
    propertiesList.insert(tk.END, f"{'ID':<5} {'Address':<30} {'Price':<15} {'Bedrooms':<10} {'Category':<30} {'Market Date':<15} {'Vendor':<20}")
    propertiesList.insert(tk.END, '-'*100)
    
    # Add each property to the listbox
    for prop in properties:
        propertiesList.insert(tk.END, f"{prop[0]:<5} {prop[1]:<30} {prop[2]:<15} {prop[3]:<10} {prop[4]:<30} {prop[5]:<15} {prop[6]:<20}")

    # Exit button for the view properties window
    tk.Button(viewWindow, text="Close Window", command=viewWindow.destroy).pack(pady=10)
    
    conn.close()
