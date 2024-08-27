import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import imageio
import threading

#Create connection with database.
def createConnection():
    """Initialize connection to the SQLite database."""
    return sqlite3.connect('properties.db')

#Function to display property listings.
def viewPropertyListingWindow():
    """Create and display the View Property Listing window."""
    viewWindow = tk.Toplevel(bg="beige")  
    viewWindow.title("View Property Listings")
    viewWindow.geometry("1920x1080")  
    tk.Label(viewWindow, text="Property Listings", font=("Helvetica", 16), bg="beige").pack(pady=20)  

    # Create the treeview to display property listings to user on the right hand side of the screen.
    #The listings should display all property features such as address, asking price, bedroom, sale status, marketed since and vendor details.
    columns = ("Address", "Asking Price"
               , "Bedrooms", "Category", "Market Date", "Vendor")
    tree = ttk.Treeview(viewWindow, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Implement framework to display property photo and property video tour on the window.
    mediaFrame = tk.Frame(viewWindow, bg="beige")  
    mediaFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    #Implemented canvas, which helped display property photos, retrieved from property database.
    photoCanvas = tk.Canvas(mediaFrame, width=600, height=300, bg="beige") 
    photoCanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    # same with property video tour.
    videoCanvas = tk.Canvas(mediaFrame, width=600, height=300, bg="beige")  
    videoCanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#Display photo and video if its retractable from database.
    def update_media(uploadedPhoto, uploadedVideo):
        if uploadedPhoto:
            image = Image.open(uploadedPhoto)
            image.thumbnail((600, 300))  
            photo = ImageTk.PhotoImage(image)
            photoCanvas.create_image(0, 0, anchor=tk.NW, image=photo)
            photoCanvas.image = photo  
        else:
            # Erase any photo content, if failed to retreived.
            photoCanvas.delete("all")  

        if uploadedVideo:
            # Started a new thread for video playback to avoid any GUI blockage.
            threading.Thread(target=playVideo, args=(uploadedVideo,)).start()
        else:
            # Erase any video content, if failed to retreived.
            videoCanvas.delete("all")  

#Plays uploaded property video to the agent on the property lisiting window.
    def playVideo(uploadedVideo):
        reader = imageio.get_reader(uploadedVideo)
        #Each frame is converted to PIL image then into a formatable video.
        delay = int(1000 / reader.get_meta_data()['fps'])
        #CALCULATES THE DELAY BETWEEN EACH VIDEO FRAME.
        for frame in reader:
            image = Image.fromarray(frame)
            image.thumbnail((600, 300))  
            photo = ImageTk.PhotoImage(image)
            videoCanvas.create_image(0, 0, anchor=tk.NW, image=photo)
            videoCanvas.image = photo  
            videoCanvas.update()
            videoCanvas.after(delay)

    # Treeview selection which helpsportray property details and photo/video to user
    def viewProperties(event):
        selectedProperty = tree.selection()
        if selectedProperty:
            item = tree.item(selectedProperty[0], 'values')
            address = item[0]  # Address is the 1st column of treeview
            # Retrieve paths to and video and photo for the selected address from the database, when property is clicked by agent.
            with createConnection() as conn:
                c = conn.cursor()
                c.execute("SELECT photo_path, video_path FROM properties WHERE address = ?", (address,))
                paths = c.fetchone()
                if paths:
                    uploadedPhoto, uploadedVideo = paths
                    update_media(uploadedPhoto, uploadedVideo)

    tree.bind("<<TreeviewSelect>>", viewProperties)

    def load_data():
        """Load data from the database into the Treeview."""
        for item in tree.get_children():
            tree.delete(item)  # Clear existing data

        # Filter property features such as bedroom number, price budgets etc.
        min_bedrooms = minBedroomsVar.get()
        max_bedrooms = maxBedroomsVar.get()
        min_price = minPriceVar.get()
        max_price = maxPriceVar.get()
        
        query = "SELECT address, asking_price, bedrooms, category, market_date, vendor FROM properties WHERE 1=1"
        params = []

        if min_bedrooms:
            query += " AND bedrooms >= ?"
            params.append(min_bedrooms)
        if max_bedrooms:
            query += " AND bedrooms <= ?"
            params.append(max_bedrooms)
        if min_price:
            query += " AND asking_price >= ?"
            params.append(min_price)
        if max_price:
            query += " AND asking_price <= ?"
            params.append(max_price)
        
        with createConnection() as conn:
            c = conn.cursor()
            c.execute(query, tuple(params))
            rows = c.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)

#Option to delete property listing from 'property listing window'
    def delete_property():
        """Delete the selected property from the database."""
        selectedProperty = tree.selection()
        if not selectedProperty:#If property is not selected, void deletion.
            messagebox.showwarning("Selection Error", "No property selected for deletion.")
            return

        property_address = tree.item(selectedProperty[0], 'values')[0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the property at {property_address}?")
        if not confirm:
            return
        
        with createConnection() as conn:
            c = conn.cursor()
            try:
                c.execute("DELETE FROM properties WHERE address = ?", (property_address,))
                conn.commit()
                load_data()  # Refresh the Treeview section by clicking refresh button after deletion
                messagebox.showinfo("Delete Property", "Property deleted successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

    #Frame for filters.
    filterFrame = tk.Frame(viewWindow, bg="beige")  # Set filter frame background to beige
    filterFrame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)
    tk.Label(filterFrame, text="Min Bedrooms:", bg="beige").grid(row=0, column=0, padx=5, pady=5)
    minBedroomsVar = tk.IntVar()
    tk.Entry(filterFrame, textvariable=minBedroomsVar).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(filterFrame, text="Max Bedrooms:", bg="beige").grid(row=0, column=2, padx=5, pady=5)
    maxBedroomsVar = tk.IntVar()
    tk.Entry(filterFrame, textvariable=maxBedroomsVar).grid(row=0, column=3, padx=5, pady=5)
    tk.Label(filterFrame, text="Min Price:", bg="beige").grid(row=1, column=0, padx=5, pady=5)
    minPriceVar = tk.IntVar()
    tk.Entry(filterFrame, textvariable=minPriceVar).grid(row=1, column=1, padx=5, pady=5)
    tk.Label(filterFrame, text="Max Price:", bg="beige").grid(row=1, column=2, padx=5, pady=5)
    maxPriceVar = tk.IntVar()
    tk.Entry(filterFrame, textvariable=maxPriceVar).grid(row=1, column=3, padx=5, pady=5)
    tk.Button(filterFrame, text="Refresh", command=load_data, bg="brown", fg="white").grid(row=2, column=0, padx=10, pady=10)  # Button color changed to brown
    tk.Button(filterFrame, text="Delete Property", command=delete_property, bg="brown", fg="white").grid(row=2, column=1, padx=10, pady=10)  # Button color changed to brown
    tk.Button(filterFrame, text="Close Window", command=viewWindow.destroy, bg="brown", fg="white").grid(row=2, column=2, padx=10, pady=10)  # Button color changed to brown

    load_data()  # Load data initially


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()  # Hide the root (propertyWindow) as is not needed

    mainWindow = tk.Toplevel()
    mainWindow.title("Main Menu")
    mainWindow.geometry("300x200")

    tk.Button(mainWindow, text="View Property Listings", command=viewPropertyListingWindow).pack(pady=10)
    tk.Button(mainWindow, text="Close", command=mainWindow.destroy).pack(pady=10)

    mainWindow.mainloop()
