import tkinter as tk
from tkinter import messagebox
import sqlite3
import sqlite3

def createConnection():
    conn = sqlite3.connect('properties.db')
    return conn

def updatePropertyWindow():
    updatePropertyListing = tk.Toplevel(bg="black")
    updatePropertyListing.title("Update Property")
    updatePropertyListing.geometry("400x400")
    updatePropertyListing.resizable(False, False)

    tk.Label(updatePropertyListing, text="Update Property Details", bg="black", fg="white").pack(pady=20)

    tk.Label(updatePropertyListing, text="Property ID:", bg="black", fg="white").pack(pady=5)
    propertyIdInput = tk.Entry(updatePropertyListing)
    propertyIdInput.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Property Address:", bg="black", fg="white").pack(pady=5)
    updateAddressInput = tk.Entry(updatePropertyListing)
    updateAddressInput.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Asking Price (£):", bg="black", fg="white").pack(pady=5)
    updatePriceInput = tk.Entry(updatePropertyListing)
    updatePriceInput.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Number of Bedrooms:", bg="black", fg="white").pack(pady=5)
    updateBedroomsInput = tk.Entry(updatePropertyListing)
    updateBedroomsInput.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Category:", bg="black", fg="white").pack(pady=5)
    updateCategoryOptions = ["For Sale", "Sold Subject to Contract", "Valuation", "Completed"]
    updateCategoryInput = tk.StringVar(value=updateCategoryOptions[0])
    updateCategoryMenu = tk.OptionMenu(updatePropertyListing, updateCategoryInput, *updateCategoryOptions)
    updateCategoryMenu.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Market Date (YYYY-MM-DD):", bg="black", fg="white").pack(pady=5)
    updateDateInput = tk.Entry(updatePropertyListing)
    updateDateInput.pack(pady=5)

    tk.Label(updatePropertyListing, text="New Vendor:", bg="black", fg="white").pack(pady=5)
    newVendorInput = tk.Entry(updatePropertyListing)
    newVendorInput.pack(pady=5)

    def submitUpdate():
        conn = createConnection()
        c = conn.cursor()
        propertyID = int(propertyIdInput.get())
        updateAddress = updateAddressInput.get()
        updateAskingPrice = float(updatePriceInput.get())
        updateBedroom = int(updateBedroomsInput.get())
        updateSaleCategory = updateCategoryInput.get()
        updateMarketDate = updateDateInput.get()
        updateVendorContact = newVendorInput.get()

        try:
            c.execute("UPDATE properties SET address=?, asking_price=?, bedrooms=?, category=?, market_date=?, vendor=? WHERE id=?",
                      (updateAddress, updateAskingPrice, updateBedroom, updateSaleCategory, updateMarketDate, updateVendorContact, propertyID))
            conn.commit()
            messagebox.showinfo("Update Listing", "Property listing updated successfully!")
            updatePropertyListing.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Update Listing", "Listing with this address already exists. Please use a different address.")
        finally:
            conn.close()

    tk.Button(updatePropertyListing, text="Submit", command=submitUpdate).pack(pady=10)
    #Close
    tk.Button(updatePropertyListing, text="Close Window", command=updatePropertyListing.destroy).pack(pady=10)
