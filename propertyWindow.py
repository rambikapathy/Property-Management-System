import tkinter as tk
from tkinter import messagebox
from faceRecognition import validateAgentFaceID, retrieveFaceID
from addProperty import addPropertyWindow
from deleteProperty import deletePropertyWindow
from updateProperty import updatePropertyWindow
from viewPropertyList import viewPropertyListingWindow
import sqlite3

#This function retreives faces stored in the faceRecognition database.
#It then compares the new face (when agent is trying to access the property listings) with faces stored in the database to validate agent authenticaiton.
def openPropertyWindow():
    """Open the property management window if face is recognized."""
    registered_faces = retrieveFaceID()
    if validateAgentFaceID(registered_faces):  
        propertyWindow = tk.Toplevel()
        propertyWindow.title("Property Window")
        propertyWindow.geometry("400x400")
        propertyWindow.resizable(False, False)
        propertyWindow.configure(bg="beige")  
#If validation is passed, authorised agent will enter property site to make changes to property listings.
        tk.Label(propertyWindow, text="Property Management System", bg="beige", fg="black", font=("Arial", 14)).pack(pady=20)

        button_options = {'bg': 'brown', 'fg': 'white'}  
        tk.Button(propertyWindow, text="Add Property Listing", command=addPropertyWindow, **button_options).pack(pady=10) #Add properties
        tk.Button(propertyWindow, text="Delete Property Listing", command=deletePropertyWindow, **button_options).pack(pady=10)# Delete properties
        tk.Button(propertyWindow, text="Update Property Listing", command=updatePropertyWindow, **button_options).pack(pady=10)#Update properties
        tk.Button(propertyWindow, text="View Property Listings", command=viewPropertyListingWindow, **button_options).pack(pady=10)# View available properties (property lising)
        tk.Button(propertyWindow, text="Close Window", command=propertyWindow.destroy, **button_options).pack(pady=20)
    else:
        #If agent's face does not match, fail validation.
        messagebox.showerror("Authentication Failed", "Face not recognized. Access denied.")

#Connection to storing and retierving property/client data from property database.
def createConnection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect('properties.db')
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return None