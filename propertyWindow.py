import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to SQLite database and create a table for properties if it doesn't exist
conn = sqlite3.connect('properties.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL UNIQUE,
                askingPrice REAL NOT NULL,
                noOfBedrooms INTEGER NOT NULL,
                category TEXT NOT NULL,
                marketDate TEXT NOT NULL,
                vendor TEXT NOT NULL
            )''')
conn.commit()

def openPropertyWindow():
    propertyWindow = tk.Toplevel(bg="black")
    propertyWindow.title("Property Window")
    propertyWindow.geometry("400x300")
    propertyWindow.resizable(False, False)  

    tk.Label(propertyWindow, text="Property Management System", bg="black", fg="white").pack(pady=20)

    tk.Button(propertyWindow, text="Add Property", command=addPropertyDetails).pack(pady=10)
    tk.Button(propertyWindow, text="Delete Property", command=deletePropertyDetails).pack(pady=10)
    tk.Button(propertyWindow, text="Update Property", command=updatePropertyDetails).pack(pady=10)

    tk.Button(propertyWindow, text="Close", command=propertyWindow.destroy).pack(pady=20)

def addPropertyDetails():
    addPropertyWindow = tk.Toplevel(bg="black")
    addPropertyWindow.title("Add Property")
    addPropertyWindow.geometry("400x400")
    addPropertyWindow.resizable(False, False)

    tk.Label(addPropertyWindow, text="Add Property Details", bg="black", fg="white").pack(pady=20)

    tk.Label(addPropertyWindow, text="Property Address:", bg="black", fg="white").pack(pady=5)
    addPropertyAddress = tk.Entry(addPropertyWindow)
    addPropertyAddress.pack(pady=5)

    tk.Label(addPropertyWindow, text="Asking Price:", bg="black", fg="white").pack(pady=5)
    addPrice = tk.Entry(addPropertyWindow)
    addPrice.pack(pady=5)

    tk.Label(addPropertyWindow, text="Number of Bedrooms:", bg="black", fg="white").pack(pady=5)
    addNoOfBedrooms = tk.Entry(addPropertyWindow)
    addNoOfBedrooms.pack(pady=5)

    tk.Label(addPropertyWindow, text="Category:", bg="black", fg="white").pack(pady=5)
    addCategory = tk.Entry(addPropertyWindow)
    addCategory.pack(pady=5)

    tk.Label(addPropertyWindow, text="Market Date (YYYY-MM-DD):", bg="black", fg="white").pack(pady=5)
    addMarketDate = tk.Entry(addPropertyWindow)
    addMarketDate.pack(pady=5)

    tk.Label(addPropertyWindow, text="Vendor:", bg="black", fg="white").pack(pady=5)
    addVendor = tk.Entry(addPropertyWindow)
    addVendor.pack(pady=5)

    def registerProperty():
        address = addPropertyAddress.get()
        askingPrice = float(addPrice.get())
        noOfBedrooms = int(addNoOfBedrooms.get())
        category = addCategory.get()
        marketDate = addMarketDate.get()
        vendor = addVendor.get()

        try:
            # Insert data into SQLite database
            c.execute("INSERT INTO properties (address, askingPrice, noOfBedrooms, category, marketDate, vendor) VALUES (?, ?, ?, ?, ?, ?)",
                      (address, askingPrice, noOfBedrooms, category, marketDate, vendor))
            conn.commit()
            messagebox.showinfo("Add Property", "Property added successfully!")
            addPropertyWindow.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Add Property", "Property with this address already exists. Please use a different address.")

    tk.Button(addPropertyWindow, text="Submit", command=registerProperty).pack(pady=10)

def deletePropertyDetails():
    deleteWindow = tk.Toplevel(bg="black")
    deleteWindow.title("Delete Property")
    deleteWindow.geometry("400x300")
    deleteWindow.resizable(False, False)

    tk.Label(deleteWindow, text="Delete Property", bg="black", fg="white").pack(pady=20)

    tk.Label(deleteWindow, text="Property ID:", bg="black", fg="white").pack(pady=5)
    propertyIdInput = tk.Entry(deleteWindow)
    propertyIdInput.pack(pady=5)

    def submitDeletion():
        property_id = int(propertyIdInput.get())
        c.execute("DELETE FROM properties WHERE id=?", (property_id,))
        conn.commit()
        messagebox.showinfo("Delete Property", "Property deleted successfully!")
        deleteWindow.destroy()

    tk.Button(deleteWindow, text="Submit", command=submitDeletion).pack(pady=10)

def updatePropertyDetails():
    updateWindow = tk.Toplevel(bg="black")
    updateWindow.title("Update Property")
    updateWindow.geometry("400x400")
    updateWindow.resizable(False, False)

    tk.Label(updateWindow, text="Update Property Details", bg="black", fg="white").pack(pady=20)

    tk.Label(updateWindow, text="Property ID:", bg="black", fg="white").pack(pady=5)
    updatePropertyId = tk.Entry(updateWindow)
    updatePropertyId.pack(pady=5)

    tk.Label(updateWindow, text="Update Property Address:", bg="black", fg="white").pack(pady=5)
    updatePropertyAddress = tk.Entry(updateWindow)
    updatePropertyAddress.pack(pady=5)

    tk.Label(updateWindow, text="Update Asking Price:", bg="black", fg="white").pack(pady=5)
    updateAskingPrice = tk.Entry(updateWindow)
    updateAskingPrice.pack(pady=5)

    tk.Label(updateWindow, text="Update Number of Bedrooms:", bg="black", fg="white").pack(pady=5)
    updateBedroomNo = tk.Entry(updateWindow)
    updateBedroomNo.pack(pady=5)

    tk.Label(updateWindow, text="Update Category:", bg="black", fg="white").pack(pady=5)
    updateCategory = tk.Entry(updateWindow)
    updateCategory.pack(pady=5)

    tk.Label(updateWindow, text="Update Market Date (YYYY-MM-DD):", bg="black", fg="white").pack(pady=5)
    updateMarketDate = tk.Entry(updateWindow)
    updateMarketDate.pack(pady=5)

    tk.Label(updateWindow, text="Update Vendor:", bg="black", fg="white").pack(pady=5)
    updateVendor = tk.Entry(updateWindow)
    updateVendor.pack(pady=5)

    def submitUpdate():
        updatedPropertyID = int(updatePropertyId.get())
        updatedPropertyAddress = updatePropertyAddress.get()
        updatedAskingPrice = float(updateAskingPrice.get())
        updatedBedroomNo = int(updateBedroomNo.get())
        updatedCategory = updateCategory.get()
        updatedMarketDate = updateMarketDate.get()
        updatedVendor = updateVendor.get()

        try:
            # Update data in SQLite database
            c.execute("UPDATE properties SET address=?, askingPrice=?, noOfBedrooms=?, category=?, marketDate=?, vendor=? WHERE id=?",
                      (updatedPropertyAddress, updatedAskingPrice, updatedBedroomNo, updatedCategory, updatedMarketDate, updatedVendor, updatedPropertyID))
            conn.commit()
            messagebox.showinfo("Update Property", "Property listing updated successfully!")
            updateWindow.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Update Property", "Property with this address already exists. Please use a different address.")

    tk.Button(updateWindow, text="Submit", command=submitUpdate).pack(pady=10)
