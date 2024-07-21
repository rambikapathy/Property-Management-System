import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

def createConnection():
    """Initialize connection to the SQLite database."""
    return sqlite3.connect('properties.db')

def createTable():
    """Create the properties table if it does not exist."""
    conn = createConnection()
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT UNIQUE NOT NULL,
            asking_price REAL NOT NULL,
            bedrooms INTEGER NOT NULL,
            category TEXT NOT NULL,
            market_date TEXT NOT NULL,
            vendor TEXT NOT NULL,
            photo_path TEXT  -- Column to store photo file path
        );
    ''')
    
    conn.commit()
    conn.close()

def addPropertyWindow():
    """Create and display the Add Property window."""
    createTable()  # Ensure the table is created before showing the window

    addProperty = tk.Toplevel(bg="black")
    addProperty.title("Add Property")
    addProperty.geometry("600x800")  # Adjust size for photo upload functionality
    addProperty.resizable(False, False)

    tk.Label(addProperty, text="Add Property Details", bg="black", fg="white", font=("Helvetica", 16)).pack(pady=20)

    tk.Label(addProperty, text="Property Address:", bg="black", fg="white").pack(pady=5)
    propertyAddressInput = tk.Entry(addProperty, width=50)
    propertyAddressInput.pack(pady=5)

    tk.Label(addProperty, text="Asking Price (£):", bg="black", fg="white").pack(pady=5)
    priceInput = tk.Entry(addProperty, width=50)
    priceInput.pack(pady=5)

    tk.Label(addProperty, text="Number of Bedrooms:", bg="black", fg="white").pack(pady=5)
    bedroomsInput = tk.Entry(addProperty, width=50)
    bedroomsInput.pack(pady=5)

    tk.Label(addProperty, text="Sale Category:", bg="black", fg="white").pack(pady=5)
    saleCategoryOptions = ["For Sale", "Sold Subject to Contract", "Valuation", "Completed"]
    saleCategoryInput = tk.StringVar(value=saleCategoryOptions[0])
    saleCategoryMenu = tk.OptionMenu(addProperty, saleCategoryInput, *saleCategoryOptions)
    saleCategoryMenu.pack(pady=5)

    tk.Label(addProperty, text="Market Date (YYYY-MM-DD):", bg="black", fg="white").pack(pady=5)
    dateInput = tk.Entry(addProperty, width=50)
    dateInput.insert(0, datetime.now().strftime('%Y-%m-%d'))
    dateInput.pack(pady=5)

    tk.Label(addProperty, text="Vendor Full Name:", bg="black", fg="white").pack(pady=5)
    vendorDetailsInput = tk.Entry(addProperty, width=50)
    vendorDetailsInput.pack(pady=5)

    # Label and button for photo upload
    tk.Label(addProperty, text="Property Photo:", bg="black", fg="white").pack(pady=5)
    propertyPhoto = tk.StringVar()
    propertyPhoto.set("No photo selected")

    photoLabel = tk.Label(addProperty, bg="black")
    photoLabel.pack(pady=5)

    def uploadPhoto():
        """Open file dialog to select and display a photo."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            propertyPhoto.set(file_path)
            # Display the selected photo
            image = Image.open(file_path)
            image.thumbnail((250, 250))  # Resize the image to fit in the window
            photo = ImageTk.PhotoImage(image)
            photoLabel.config(image=photo)
            photoLabel.image = photo  # Keep a reference to avoid garbage collection

    tk.Button(addProperty, text="Upload Photo", command=uploadPhoto).pack(pady=5)
    tk.Label(addProperty, textvariable=propertyPhoto, bg="black", fg="white").pack(pady=5)

    def submitProperty():
        conn = createConnection()
        c = conn.cursor()

        propertyAddress = propertyAddressInput.get().strip()
        askingPrice = priceInput.get().strip()
        bedrooms = bedroomsInput.get().strip()
        saleCategory = saleCategoryInput.get()
        marketDate = dateInput.get().strip()
        vendorDetails = vendorDetailsInput.get().strip()
        photoFilePath = propertyPhoto.get()
        
        #All entry boxes must be filled inorder for property to be succesfully added
        if not propertyAddress or not askingPrice or not bedrooms or not marketDate or not vendorDetails:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

        if photoFilePath == "No photo selected":
            messagebox.showwarning("Photo Missing", "No photo selected. Proceeding without a photo.")
            photoFilePath = None

        try:
            askingPrice = float(askingPrice)
            bedrooms = int(bedrooms)
        except ValueError:
            messagebox.showerror("Input Error", "Asking Price and Number of Bedrooms must be numeric.")
            return

        try:
            datetime.strptime(marketDate, '%Y-%m-%d')  # Validate date format
        except ValueError:
            messagebox.showerror("Input Error", "Market Date must be in YYYY-MM-DD format.")
            return

        try:
            c.execute("INSERT INTO properties (address, asking_price, bedrooms, category, market_date, vendor, photo_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (propertyAddress, askingPrice, bedrooms, saleCategory, marketDate, vendorDetails, photoFilePath))
            conn.commit()
            messagebox.showinfo("Add Property Listing", "Property listing added successfully!")
            addProperty.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Add Property Listing", "Property listing with this address already exists. Please use a different address.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    tk.Button(addProperty, text="Submit", command=submitProperty).pack(pady=10)
    tk.Button(addProperty, text="Close Window", command=addProperty.destroy).pack(pady=10)

if __name__ == '__main__':
    createTable()
