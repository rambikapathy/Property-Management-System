import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


#Initialize connection to database
def createConnection():
    conn = sqlite3.connect('properties.db')
    return conn


def addPropertyWindow():
    addProperty = tk.Toplevel(bg="black")
    addProperty.title("Add Property")
    addProperty.geometry("600x600")
    addProperty.resizable(False, False)

    tk.Label(addProperty, text="Add Property Details", bg="black", fg="white").pack(pady=20)

    tk.Label(addProperty, text="Property Address:", bg="black", fg="white").pack(pady=5)
    propertyAddressInput = tk.Entry(addProperty)
    propertyAddressInput.pack(pady=5)

    tk.Label(addProperty, text="Asking Price (£):", bg="black", fg="white").pack(pady=5)
    priceInput = tk.Entry(addProperty)
    priceInput.pack(pady=5)

    tk.Label(addProperty, text="Number of Bedrooms:", bg="black", fg="white").pack(pady=5)
    bedroomsInput = tk.Entry(addProperty)
    bedroomsInput.pack(pady=5)

    tk.Label(addProperty, text="Sale Category:", bg="black", fg="white").pack(pady=5)
    saleCategoryOptions = ["For Sale", "Sold Subject to Contract", "Valuation", "Completed"]
    saleCategoryInput = tk.StringVar(value=saleCategoryOptions[0])
    saleCategoryMenu = tk.OptionMenu(addProperty, saleCategoryInput, *saleCategoryOptions)
    saleCategoryMenu.pack(pady=5)

    tk.Label(addProperty, text="Market Date (YYYY-MM-DD):", bg="black", fg="white").pack(pady=5)
    dateInput = tk.Entry(addProperty)
    dateInput.insert(0, datetime.now().strftime('%Y-%m-%d'))
    dateInput.pack(pady=5)

    tk.Label(addProperty, text="Vendor Full Name:", bg="black", fg="white").pack(pady=5)
    vendorDetailsInput = tk.Entry(addProperty)
    vendorDetailsInput.pack(pady=5)

    def submitProperty():
        conn = createConnection()
        c = conn.cursor()
        propertyAddress = propertyAddressInput.get()
        askingPrice = float(priceInput.get())
        bedrooms = int(bedroomsInput.get())
        saleCategory = saleCategoryInput.get()
        marketDate = dateInput.get()
        vendorDetails = vendorDetailsInput.get()

        try:
            c.execute("INSERT INTO properties (propertyAddress, askingPrice, bedrooms, category, market_date, vendor) VALUES (?, ?, ?, ?, ?, ?)",
                      (propertyAddress, askingPrice, bedrooms, saleCategory, marketDate, vendorDetails))
            conn.commit()
            messagebox.showinfo("Add Property Listing", "Property listing added successfully!")
            addProperty.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Add Property Listing", "Property listing with this address already exists. Please use a different address.")
        finally:
            conn.close()

    tk.Button(addProperty, text="Submit", command=submitProperty).pack(pady=10)

    # Exit button for the add property window
    tk.Button(addProperty, text="Close Window", command=addProperty.destroy).pack(pady=10)
