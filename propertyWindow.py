import tkinter as tk
from addProperty import addPropertyWindow
from deleteProperty import deletePropertyWindow
from updateProperty import updatePropertyWindow
from viewPropertyList import viewPropertyListWindow

def openPropertyWindow():
    propertyWindow = tk.Toplevel(bg="black")
    propertyWindow.title("Property Window")
    propertyWindow.geometry("400x400")
    propertyWindow.resizable(False, False)  

    tk.Label(propertyWindow, text="Property Management System", bg="black", fg="white").pack(pady=20)

    tk.Button(propertyWindow, text="Add Property Listing", command=lambda: addPropertyWindow()).pack(pady=10)
    tk.Button(propertyWindow, text="Delete Property Listing", command=lambda: deletePropertyWindow()).pack(pady=10)
    tk.Button(propertyWindow, text="Update Property Listing", command=lambda: updatePropertyWindow()).pack(pady=10)
    tk.Button(propertyWindow, text="View Property Listings", command=lambda: viewPropertyListWindow()).pack(pady=10)

    tk.Button(propertyWindow, text="Close Window", command=propertyWindow.destroy).pack(pady=20)

def createConnection():
    import sqlite3
    conn = sqlite3.connect('properties.db')
    return conn

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Property Management System")
    root.geometry("400x300")
    root.configure(bg="black")

    tk.Button(root, text="Open Property Window", command=openPropertyWindow).pack(pady=20)

    root.mainloop()
