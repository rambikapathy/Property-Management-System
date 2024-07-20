import tkinter as tk
from tkinter import messagebox
import sqlite3

def createConnection():
    conn = sqlite3.connect('properties.db')
    return conn

def deletePropertyWindow():
    deleteProperty = tk.Toplevel(bg="black")
    deleteProperty.title("Delete Property")
    deleteProperty.geometry("400x300")
    deleteProperty.resizable(False, False)

    tk.Label(deleteProperty, text="Delete Property", bg="black", fg="white").pack(pady=20)

#Create unique property ID for each property listing
    tk.Label(deleteProperty, text="Property ID:", bg="black", fg="white").pack(pady=5)
    propertyIdInput = tk.Entry(deleteProperty)
    propertyIdInput.pack(pady=5)

    def submitDeletion():
        conn = createConnection()
        c = conn.cursor()
        property_id = int(propertyIdInput.get())
        c.execute("DELETE FROM properties WHERE id=?", (property_id,))
        conn.commit()
        messagebox.showinfo("Delete Property", "Property deleted successfully!")
        deleteProperty.destroy()
        conn.close()

    tk.Button(deleteProperty, text="Submit", command=submitDeletion).pack(pady=10)

    # Close window
    tk.Button(deleteProperty, text="Close Window", command=deleteProperty.destroy).pack(pady=10)
