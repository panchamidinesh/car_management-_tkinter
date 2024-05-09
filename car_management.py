import sqlite3   #SQLite is a lightweight, serverless database engine that stores data in a local file.
import tkinter as tk  #tandard Python library for creating graphical user interfaces (GUIs).
from tkinter import messagebox, PhotoImage
from tkinter import *

# Create SQLite database connection
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

# Create cars table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
    VIN INTEGER PRIMARY KEY,
    Brand TEXT,
    Model TEXT,
    Year INTEGER)''')
conn.commit()

def add_car():
    brand = brand_entry.get().strip()   #The .get() method retrieves the content of the input field,.strip() removes any leading or trailing whitespace.
    model = model_entry.get().strip()
    year = year_entry.get().strip()

    if not (brand and model and year):  
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        year = int(year)
    except ValueError:
        messagebox.showerror("Error", "Year must be a valid integer.")
        return

    try:
        cursor.execute("INSERT INTO cars (Brand, Model, Year) VALUES (?, ?, ?)", (brand, model, year))
        conn.commit()
        messagebox.showinfo("Success", "Car added successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to add car: {e}")

def delete_car():
    vin = vin_entry.get().strip()  #vehicle identification number  , strip() removes any leading or trailing whitespace.

    if not vin:
        messagebox.showerror("Error", "Please enter the VIN.")
        return

    try:
        vin = int(vin)
    except ValueError:
        messagebox.showerror("Error", "VIN must be a valid integer.")
        return

    try:
        cursor.execute("DELETE FROM cars WHERE VIN=?", (vin,))
        conn.commit()
        messagebox.showinfo("Success", "Car deleted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to delete car: {e}")

def update_car():
    vin = update_vin_entry.get().strip()
    brand = update_brand_entry.get().strip()
    model = update_model_entry.get().strip()
    year = update_year_entry.get().strip()

    if not (vin and brand and model and year):
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        vin = int(vin)
        year = int(year)
    except ValueError:
        messagebox.showerror("Error", "VIN and Year must be valid integers.")
        return

    try:
        cursor.execute("UPDATE cars SET Brand=?, Model=?, Year=? WHERE VIN=?", (brand, model, year, vin))  # cursor.execute("UPDATE cars SET Brand=?, Model=?, Year=? WHERE VIN=?", (brand, model, year, vin))
        conn.commit()
        messagebox.showinfo("Success", "Car updated successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to update car: {e}")

def search_cars():
    search_term = search_entry.get().strip()
    vin = vin_search_entry.get().strip()  # Get the VIN search term

    if not (search_term or vin):   #This line checks if both the search_term and vin are empty (i.e., not provided by the user).
        messagebox.showerror("Error", "Please enter a search term or VIN.")
        return

    try:
        if search_term and vin:
            cursor.execute("SELECT * FROM cars WHERE (Brand LIKE ? OR Model LIKE ?) AND VIN=?", ('%' + search_term + '%', '%' + search_term + '%', vin))
            # % is used to search for records where the brand or model partially matches the provided search term
        elif search_term:
            cursor.execute("SELECT * FROM cars WHERE Brand LIKE ? OR Model LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
        else:
            cursor.execute("SELECT * FROM cars WHERE VIN=?", (vin,))
        
        cars = cursor.fetchall()

        if cars:
            result_text.config(state=tk.NORMAL)   
            result_text.delete('1.0', tk.END)    
            for car in cars:
                result_text.insert(tk.END, f"VIN: {car[0]}, Brand: {car[1]}, Model: {car[2]}, Year: {car[3]}\n")
            result_text.config(state=tk.DISABLED)  
        else:
            messagebox.showinfo("No Results", "No car found matching the search criteria.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Failed to search car: {e}")


root = tk.Tk()
root.title("Car Management System")

# Load the background image
background_image = PhotoImage(file="car_back.png")

# Set the background image
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
# Set font style to italic
font_style = ('Arial', 10, 'italic')

# Add heading
heading_label = tk.Label(root, text="  CAR MANAGEMENT SYSTEM  ", font=("Arial", 17, "bold"), bg="#FFF2D7")
heading_label.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")  # Changed sticky to "nsew" for center alignment  ,It spans 5 columns (from column 0 to column 4) horizontally.


# Add Car Section
add_frame = tk.LabelFrame(root, text="Add Car", padx=10, pady=5, bg="#CA8787")  #horizontal: 10, vertical: 5).
add_frame.grid(row=1, column=0, padx=10, pady=(30, 10), sticky="nsew")  # (north, south, east, west)

brand_label = tk.Label(add_frame, text="Brand:", bg="#CA8787", font=font_style)
brand_label.grid(row=0, column=0, sticky="w")  #“w” (west), aligning the label to the left.
brand_entry = tk.Entry(add_frame, font=font_style)
brand_entry.grid(row=0, column=1, padx=5, pady=2)

model_label = tk.Label(add_frame, text="Model:", bg="#CA8787", font=font_style)
model_label.grid(row=1, column=0, sticky="w")
model_entry = tk.Entry(add_frame, font=font_style)
model_entry.grid(row=1, column=1, padx=5, pady=2)

year_label = tk.Label(add_frame, text="Year:", bg="#CA8787", font=font_style)
year_label.grid(row=2, column=0, sticky="w")
year_entry = tk.Entry(add_frame, font=font_style)
year_entry.grid(row=2, column=1, padx=5, pady=2)

add_button = tk.Button(add_frame, text="Add Car", command=add_car, bg="white", font=font_style)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

# Delete Car Section
delete_frame = tk.LabelFrame(root, text="Delete Car", padx=5, pady=5, bg="#FFD0D0")
delete_frame.grid(row=2, column=0, padx=5, pady=(30,5), sticky="nsew")

vin_label = tk.Label(delete_frame, text="VIN:", bg="#FFD0D0", font=font_style)
vin_label.grid(row=0, column=0, sticky="w")
vin_entry = tk.Entry(delete_frame, font=font_style)
vin_entry.grid(row=0, column=1, padx=5, pady=2)

delete_button = tk.Button(delete_frame, text="Delete Car", command=delete_car, bg="white", font=font_style)
delete_button.grid(row=1, column=0, columnspan=1, pady=5)

# Update Car Section
update_frame = tk.LabelFrame(root, text="Update Car", padx=10, pady=5, bg="#A87676")
update_frame.grid(row=1, column=1, padx=10, pady=(30, 10), sticky="nsew")

update_vin_label = tk.Label(update_frame, text="VIN:", bg="#A87676", font=font_style)
update_vin_label.grid(row=0, column=0, sticky="w")
update_vin_entry = tk.Entry(update_frame, font=font_style)
update_vin_entry.grid(row=0, column=1, padx=5, pady=2)

update_brand_label = tk.Label(update_frame, text="Brand:", bg="#A87676", font=font_style)
update_brand_label.grid(row=1, column=0, sticky="w")
update_brand_entry = tk.Entry(update_frame, font=font_style)
update_brand_entry.grid(row=1, column=1, padx=5, pady=2)

update_model_label = tk.Label(update_frame, text="Model:", bg="#A87676", font=font_style)
update_model_label.grid(row=2, column=0, sticky="w")
update_model_entry = tk.Entry(update_frame, font=font_style)
update_model_entry.grid(row=2, column=1, padx=5, pady=2)

update_year_label = tk.Label(update_frame, text="Year:", bg="#A87676", font=font_style)
update_year_label.grid(row=3, column=0, sticky="w")
update_year_entry = tk.Entry(update_frame, font=font_style)
update_year_entry.grid(row=3, column=1, padx=5, pady=2)

update_button = tk.Button(update_frame, text="Update Car", command=update_car, bg="white", font=font_style)
update_button.grid(row=4, column=0, columnspan=2, pady=5)

# Search Car Section
search_frame = tk.LabelFrame(root, text="Search Car", padx=10, pady=5, bg="#E1ACAC")
search_frame.grid(row=1, column=2, padx=10, pady=(30, 10), sticky="ne")

search_label = tk.Label(search_frame, text="SEARCH BRAND NAME:", bg="#E1ACAC", font=font_style)
search_label.grid(row=0, column=0, sticky="w")
search_entry = tk.Entry(search_frame, font=font_style)
search_entry.grid(row=0, column=1, padx=5, pady=2)

vin_search_label = tk.Label(search_frame, text="SEARCH BY VIN:", bg="#E1ACAC", font=font_style)
vin_search_label.grid(row=1, column=0, sticky="w")
vin_search_entry = tk.Entry(search_frame, font=font_style)
vin_search_entry.grid(row=1, column=1, padx=5, pady=2)

search_button = tk.Button(search_frame, text="Search", command=search_cars, bg="white", font=font_style)
search_button.grid(row=2, column=0, columnspan=2, pady=5)

result_text = tk.Text(search_frame, height=8, width=50, state=tk.DISABLED, bg="white", font=font_style)
result_text.grid(row=3, column=0, columnspan=2, padx=5, pady=2)


root.mainloop()

# Close the database connection
conn.close()




