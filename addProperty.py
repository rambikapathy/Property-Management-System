import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import imageio
import threading

#Make connection to property database.
def createConnection():
    """Initialize connection to the SQLite database."""
    return sqlite3.connect('properties.db')

#If table for storing active system logs does not exist. 
# Create table by implementing a cursor, and execute  SQL query to create the table. The table will store the log ID, date/time, username, and log action.
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

#Function to keep track of user adding properties. The actions will then be stored to the systemLog database.
def log_action(user, action):
    """Log actions in the system_log table."""
    conn = createConnection()
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO system_log (timestamp, user, action) VALUES (?, ?, ?)",
              (timestamp, user, action))
    conn.commit()
    conn.close()

#Iniaite property table within property database, if it doesnt exist.
#Ensure the  queries in the table keep note of properety features.
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
            photo_path TEXT,
            video_path TEXT  -- Column to store video file path
        );
    ''')
    
    conn.commit()
    conn.close()

def addPropertyWindow():
    """Create and display the Add Property window."""
    createLogTable()  # Ensure the log table is created
    createTable()  
    # Ensure the table is created before showing the window

    addProperty = tk.Toplevel(bg="beige")  
    addProperty.title("Add Property")
    addProperty.geometry("700x970")  
    addProperty.resizable(False, False)

#Ask agent to input property features in the relevant fields.
    tk.Label(addProperty, text="Add Property Details", bg="beige", fg="black", font=("Helvetica", 16)).pack(pady=20)

    tk.Label(addProperty, text="Property Address:", bg="beige", fg="black").pack(pady=5)
    propertyAddressInput = tk.Entry(addProperty, width=50)
    propertyAddressInput.pack(pady=5)

    tk.Label(addProperty, text="Asking Price (£):", bg="beige", fg="black").pack(pady=5)
    priceInput = tk.Entry(addProperty, width=50)
    priceInput.pack(pady=5)

    tk.Label(addProperty, text="Number of Bedrooms:", bg="beige", fg="black").pack(pady=5)
    bedroomsInput = tk.Entry(addProperty, width=50)
    bedroomsInput.pack(pady=5)

    tk.Label(addProperty, text="Sale Category:", bg="beige", fg="black").pack(pady=5)
    saleCategoryOptions = ["For Sale", "Sold Subject to Contract", "Valuation", "Completed"]
    saleCategoryInput = tk.StringVar(value=saleCategoryOptions[0])
    saleCategoryMenu = tk.OptionMenu(addProperty, saleCategoryInput, *saleCategoryOptions)
    saleCategoryMenu.pack(pady=5)

    tk.Label(addProperty, text="Market Date (YYYY-MM-DD):", bg="beige", fg="black").pack(pady=5)
    dateInput = tk.Entry(addProperty, width=50)
    dateInput.insert(0, datetime.now().strftime('%Y-%m-%d'))
    dateInput.pack(pady=5)

    tk.Label(addProperty, text="Vendor Full Name:", bg="beige", fg="black").pack(pady=5)
    vendorDetailsInput = tk.Entry(addProperty, width=50)
    vendorDetailsInput.pack(pady=5)

    tk.Label(addProperty, text="Property Photo:", bg="beige", fg="black").pack(pady=5)
    propertyPhoto = tk.StringVar()
    propertyPhoto.set("No photo selected")

    photoLabel = tk.Label(addProperty, bg="beige")
    photoLabel.pack(pady=5)

#Upload Photo
    def uploadPhoto():
        """Open file dialog to select and display a photo."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            propertyPhoto.set(file_path)
            # Display the selected photo
            image = Image.open(file_path)
            image.thumbnail((250, 250))  
            photo = ImageTk.PhotoImage(image)
            photoLabel.config(image=photo)
            # Keep a reference of the property image, incase of avoiding garbage collection
            photoLabel.image = photo  

    tk.Button(addProperty, text="Upload Photo", command=uploadPhoto, bg="brown", fg="white").pack(pady=5)  # Button color changed to brown
    tk.Label(addProperty, textvariable=propertyPhoto, bg="beige", fg="black").pack(pady=5)

    # Video upload
    tk.Label(addProperty, text="Property Tour Video:", bg="beige", fg="black").pack(pady=5)
    propertyVideo = tk.StringVar()
    propertyVideo.set("No video selected")

    videoLabel = tk.Label(addProperty, bg="beige")
    videoLabel.pack(pady=5)

#Upload video and play the video in property listing window.
    def play_video(video_path):
        """Play the uploaded video in a loop."""
        reader = imageio.get_reader(video_path)
        delay = int(1000 / reader.get_meta_data()['fps'])
        for frame in reader:
            image = Image.fromarray(frame)
            image.thumbnail((250, 250))  
            photo = ImageTk.PhotoImage(image)
            videoLabel.config(image=photo)
            # Keep a reference to avoid garbage collection
            videoLabel.image = photo  
            videoLabel.update()
            videoLabel.after(delay)

    def uploadVideo():
        """Open file dialog to select and display a video."""
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if file_path:
            propertyVideo.set(file_path)
            videoLabel.config(text=f"Selected video: {file_path}")
            # Start a new thread to play the video again
            threading.Thread(target=play_video, args=(file_path,), daemon=True).start()

    tk.Button(addProperty, text="Upload Property Tour Video", command=uploadVideo, bg="brown", fg="white").pack(pady=5) 
    tk.Label(addProperty, textvariable=propertyVideo, bg="beige", fg="black").pack(pady=5)

#Function to store property features in property database.
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
        videoFilePath = propertyVideo.get()
        
        # All entry fields must be filled in order for property to be successfully added
        #Failure will result in error message being thrown.
        if not propertyAddress or not askingPrice or not bedrooms or not marketDate or not vendorDetails:
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return

#Uploading photo and video of property listing is required for the listing to be valid and ready to be published on the agent's website.
        if photoFilePath == "No photo selected":
            messagebox.showwarning("Photo Missing", "No photo selected. Proceeding without a photo.")
            photoFilePath = None

        if videoFilePath == "No video selected":
            messagebox.showwarning("Video Missing", "No video selected. Proceeding without a video.")
            videoFilePath = None

        try:
            askingPrice = float(askingPrice)
            bedrooms = int(bedrooms)
        except ValueError:
            messagebox.showerror("Input Error", "Asking Price and Number of Bedrooms must be numeric.")
            return

        try:
            # Validate date format t0 year-month-date.
            datetime.strptime(marketDate, '%Y-%m-%d')  
        except ValueError:
            messagebox.showerror("Input Error", "Market Date must be in YYYY-MM-DD format.")
            return

        try:
            c.execute("INSERT INTO properties (address, asking_price, bedrooms, category, market_date, vendor, photo_path, video_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (propertyAddress, askingPrice, bedrooms, saleCategory, marketDate, vendorDetails, photoFilePath, videoFilePath))
            conn.commit()
            log_action('User1', f'Added property: {propertyAddress}')  
            messagebox.showinfo("Add Property Listing", "Property listing added successfully!")
            addProperty.destroy()
        except sqlite3.IntegrityError:#If property listing with same address exists, void creation of listing.
            messagebox.showerror("Add Property Listing", "Property listing with this address already exists. Please use a different address.")
        except sqlite3.Error as e:#Throw error, if property cannot be uplaoded to database.
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    tk.Button(addProperty, text="Submit", command=submitProperty, bg="brown", fg="white").pack(pady=10)  
    tk.Button(addProperty, text="Close Window", command=addProperty.destroy, bg="brown", fg="white").pack(pady=10)  

if __name__ == '__main__':
    createTable()
    createLogTable()  # Ensure the log table is created and closed where necessary.

