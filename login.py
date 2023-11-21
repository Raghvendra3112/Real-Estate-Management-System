import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
from tkinter import StringVar
from flask.views import View
from matplotlib.backend_bases import ShowBase
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyttsx3
from xlwings import view

class ThemedToplevel(tk.Toplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#4D4C7D")  # Background color
        style = ttk.Style(self)
        style.configure("TLabel", background="#4D4C7D", foreground="#ECE3CE", font=("Segoe UI", 12))  # Updated font
        style.configure("TButton", background="#F99417", foreground="#4D4C7D", font=("Segoe UI", 14))  # Updated font
        style.configure("TRadiobutton", background="#4D4C7D", foreground="#ECE3CE", font=("Segoe UI", 12))  # Updated font
        style.layout("TButton", [
            ("Button.button", {"children":
                [("Button.focus", {"children":
                    [("Button.padding", {"children":
                        [("Button.label", {"side": "left", "expand": 1})]
                    })]
                })]
            })
        ])

def readn(nstr):
    engine = pyttsx3.init()

    engine.setProperty('voice', "english+f5")
    engine.setProperty('rate', 130)

    engine.say(nstr)
    engine.runAndWait()
    engine.stop()

class AdminDashboard(ThemedToplevel):
    def __init__(self, master, username, cursor, connection):
        super().__init__(master)
        self.title("Admin Dashboard")
        self.geometry("380x200")

        self.username = username
        self.c = cursor
        self.conn = connection

        self.admin_label = ttk.Label(self, text=f"Welcome {username} to Admin Dashboard", font=("Segoe UI", 16))
        self.logout_button = ttk.Button(self, text="Logout", command=self.logout)

        self.project_details_button = ttk.Button(self, text="Project Details", command=self.open_project_details)
        self.payment_details_button = ttk.Button(self, text="Payment Details", command=self.open_payment_details)
        self.booking_details_button = ttk.Button(self, text="Booking Details", command=self.open_booking_details)
        self.area_calculator_button = ttk.Button(self, text="Area Calculator", command=self.open_area_calculator)

        self.admin_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.project_details_button.grid(row=1, column=0, pady=5, padx=5)
        self.payment_details_button.grid(row=1, column=1, pady=5, padx=5)
        self.booking_details_button.grid(row=2, column=0, pady=5, padx=5)
        self.area_calculator_button.grid(row=2, column=1, pady=5, padx=5)
        self.logout_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Create new tables
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsbooked (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsavailable (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")

    def logout(self):
        self.destroy()

    def open_project_details(self):
        project_details_window = ProjectDetailsWindow(self, self.c, self.conn)
        project_details_window.mainloop()

    def open_payment_details(self):
        payment_details_window = PaymentDetailsWindow(self, self.c, self.conn)
        payment_details_window.mainloop()

    def open_booking_details(self):
        booking_details_window = BookingDetailsWindow(self, self.c, self.conn)
        booking_details_window.mainloop()

    def open_area_calculator(self):
        area_calculator_window = AreaCalculatorWindow(self)
        area_calculator_window.mainloop()

class AreaCalculatorWindow(ThemedToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Area Calculator")
        self.geometry("350x250")

        self.value_var = tk.DoubleVar()
        self.value_var.set(1)  # Default value

        value_label = ttk.Label(self, text="Enter Value:")
        value_label.pack(pady=5)

        value_entry = ttk.Entry(self, textvariable=self.value_var)
        value_entry.pack(pady=5)

        # Dropdown for selecting the input unit
        unit_label = ttk.Label(self, text="Select Input Unit:")
        unit_label.pack(pady=5)

        self.unit_var = tk.StringVar()
        self.unit_var.set("Square Feet")  # Default input unit

        self.unit_dropdown = ttk.Combobox(self, textvariable=self.unit_var, values=["Square Feet", "Square Meter", "Acre", "Hectare", "Gaj", "Square Yard"])
        self.unit_dropdown.pack(pady=5)

        # Dropdown for selecting the output unit
        output_unit_label = ttk.Label(self, text="Select Output Unit:")
        output_unit_label.pack(pady=5)

        self.output_unit_var = tk.StringVar()
        self.output_unit_var.set("Square Feet")  # Default output unit

        self.output_unit_dropdown = ttk.Combobox(self, textvariable=self.output_unit_var, values=["Square Feet", "Square Meter", "Acre", "Hectare", "Gaj", "Square Yard"])
        self.output_unit_dropdown.pack(pady=5)

        calculate_button = ttk.Button(self, text="Calculate", command=self.calculate_area)
        calculate_button.pack(pady=10)

    def calculate_area(self):
        input_unit = self.unit_var.get()
        output_unit = self.output_unit_var.get()
        value = self.value_var.get()

        # Conversion factors (approximate values)
        conversion_factors = {
            "Square Feet": 1,
            "Square Meter": 0.092903,
            "Acre": 2.2957e-5,
            "Hectare": 9.2903e-6,
            "Gaj": 0.111111,
            "Square Yard": 0.111111
        }

        # Perform the conversion
        result = value * conversion_factors[input_unit] / conversion_factors[output_unit]
        result_text = f"Calculation Result: {result:.4f} {output_unit}"

        # Show the result in a messagebox
        messagebox.showinfo("Area Calculation Result", result_text)
        readn(result_text)

class CustomerDashboard(ThemedToplevel):
    def __init__(self, master, username, cursor, connection):
        super().__init__(master)
        self.title("Customer Dashboard")
        self.geometry("400x200")

        self.username = username
        self.c = cursor
        self.conn = connection

        self.customer_label = ttk.Label(self, text=f"Welcome {username} to Customer Dashboard", font=("Helvetica", 16))
        self.logout_button = ttk.Button(self, text="Logout", command=self.logout)
        self.project_details_button = ttk.Button(self, text="View Projects", command=self.open_project_details)
        self.payment_details_button = ttk.Button(self, text="Booking", command=self.open_payment_details)
        self.booking_details_button = ttk.Button(self, text="View Payment Details", command=self.open_booking_details)
        self.area_calculator_button = ttk.Button(self, text="Area Calculator", command=self.open_area_calculator)

        self.customer_label.grid(row=0, column=0, columnspan=4, pady=10)
        self.project_details_button.grid(row=1, column=0, pady=5, padx=5)
        self.payment_details_button.grid(row=1, column=1, pady=5, padx=5)
        self.booking_details_button.grid(row=2, column=0, pady=5, padx=5)
        self.area_calculator_button.grid(row=2, column=1, pady=5, padx=5)
        self.logout_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Create new tables
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsbooked (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsavailable (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")

    def logout(self):
        self.destroy()

    def open_project_details(self):
        project_details_window = ViewProjectWindow(self, self.c, self.conn)
        project_details_window.mainloop()

    def open_payment_details(self):
        payment_details_window = BookingWindow(self, self.c, self.conn, self.username)
        payment_details_window.mainloop()

    def open_booking_details(self):
        booking_details_window = ViewPaymentDetails2Window(self, self.username, self.c, self.conn)
        booking_details_window.mainloop()

    def open_area_calculator(self):
        area_calculator_window = AreaCalculatorWindow(self)
        area_calculator_window.mainloop()

class ViewProjectWindow(tk.Toplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("View Projects")
        self.geometry("900x300")
        self.configure(bg="#4D4C7D")
        self.c = cursor
        self.conn = connection

        self.project_label = ttk.Label(self, text="Projects Booked", font=("Segoe UI", 16))
        self.project_tree = ttk.Treeview(self, columns=("Name", "Block", "Flat No", "Price"), show="tree")

        self.project_tree.heading("#0", text="Property Name")
        self.project_tree.heading("Name", text="Name")
        self.project_tree.heading("Block", text="Block")
        self.project_tree.heading("Flat No", text="Flat No")
        self.project_tree.heading("Price", text="Price")

        self.project_tree.pack(pady=10)

        # Call a method to populate treeview with project details
        self.populate_project_tree()

    def populate_project_tree(self):
        # Fetch and display project details from the database
        self.c.execute("SELECT * FROM projectsavailable")
        projects = self.c.fetchall()

        # Dictionary to store project details based on property and block
        project_dict = {}

        for project in projects:
            property_name, block, flat_no, price = project
            if property_name not in project_dict:
                project_dict[property_name] = {}
            if block not in project_dict[property_name]:
                project_dict[property_name][block] = []
            project_dict[property_name][block].append((flat_no, price))

        # Populate the Treeview with the project details
        for property_name, blocks in project_dict.items():
            property_node = self.project_tree.insert("", "end", text=property_name)
            for block, flats in blocks.items():
                block_node = self.project_tree.insert(property_node, "end", text=block)
                for flat_no, price in flats:
                    self.project_tree.insert(block_node, "end", values=(property_name, block, flat_no, price))


class BookingWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection, username):
        super().__init__(master)
        self.title("Booking")
        self.geometry("400x500")
        self.configure(bg="#4D4C7D")
        self.c = cursor
        self.conn = connection
        self.username = username

        self.booking_label = ttk.Label(self, text="Booking Details", font=("Helvetica", 16))

        # Entry widgets for property name, block, and flat number
        self.property_label = ttk.Label(self, text="Property Name:")
        self.property_var = tk.StringVar()
        self.property_entry = ttk.Entry(self, textvariable=self.property_var)

        self.block_label = ttk.Label(self, text="Block:")
        self.block_var = tk.StringVar()
        self.block_entry = ttk.Entry(self, textvariable=self.block_var)

        self.flat_no_label = ttk.Label(self, text="Flat No:")
        self.flat_no_var = tk.StringVar()
        self.flat_no_entry = ttk.Entry(self, textvariable=self.flat_no_var)

        self.email_label = ttk.Label(self, text="Email:")
        self.email_entry = ttk.Entry(self)

        self.phone_label = ttk.Label(self, text="Phone No:")
        self.phone_entry = ttk.Entry(self)

        self.address_label = ttk.Label(self, text="Address:")
        self.address_entry = ttk.Entry(self)

        self.aadhar_label = ttk.Label(self, text="Aadhar No:")
        self.aadhar_entry = ttk.Entry(self)

        self.bank_name_label = ttk.Label(self, text="Bank Name:")
        self.bank_name_entry = ttk.Entry(self)

        self.amount_label = ttk.Label(self, text="Amount:")
        self.amount_entry = ttk.Entry(self)

        self.book_button = ttk.Button(self, text="Book Property", command=self.book_property)

        self.booking_label.pack(pady=10)

        self.property_label.pack(pady=5)
        self.property_entry.pack(pady=5)

        self.block_label.pack(pady=5)
        self.block_entry.pack(pady=5)

        self.flat_no_label.pack(pady=5)
        self.flat_no_entry.pack(pady=5)

        self.email_label.pack(pady=5)
        self.email_entry.pack(pady=5)

        self.phone_label.pack(pady=5)
        self.phone_entry.pack(pady=5)

        self.address_label.pack(pady=5)
        self.address_entry.pack(pady=5)

        self.aadhar_label.pack(pady=5)
        self.aadhar_entry.pack(pady=5)

        self.bank_name_label.pack(pady=5)
        self.bank_name_entry.pack(pady=5)

        self.amount_label.pack(pady=5)
        self.amount_entry.pack(pady=5)

        self.book_button.pack(pady=10)

    def book_property(self):
        # Get selected values from entry widgets
        selected_property = self.property_var.get()
        selected_block = self.block_var.get()
        selected_flat_no = self.flat_no_var.get()

        email = self.email_entry.get()
        phone_no = self.phone_entry.get()
        address = self.address_entry.get()
        aadhar_no = self.aadhar_entry.get()
        bank_name = self.bank_name_entry.get()
        amount = self.amount_entry.get()

        # Validate input if needed

        # Check if all required fields are filled
        if not selected_property or not selected_block or not selected_flat_no:
            messagebox.showerror("Error", "Please enter property name, block, and flat number before booking.")
            return

        # Perform the booking and payment processing here
        # You can update the database or perform any other necessary actions

        # Insert the booking details into the bookingdetails table
        self.c.execute("""
            INSERT INTO bookingdetails 
            (customer_name, email, phone_no, address, aadhar_no, property_name, block_name, flat_no, bank_name, amount) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.username, email, phone_no, address, aadhar_no, selected_property, selected_block, selected_flat_no, bank_name, amount))

        # Check if the entry already exists in projectsbooked
        self.c.execute("SELECT * FROM projectsbooked WHERE name = ? AND block = ? AND flat_no = ?",
                        (selected_property, selected_block, selected_flat_no))
        existing_entry = self.c.fetchone()

        if existing_entry:
            # Entry exists, perform update
            self.c.execute("UPDATE projectsbooked SET price = ? WHERE name = ? AND block = ? AND flat_no = ?",
                            (amount, selected_property, selected_block, selected_flat_no))
        else:
            # Entry doesn't exist, perform insert
            self.c.execute("INSERT INTO projectsbooked (name, block, flat_no, price) VALUES (?, ?, ?, ?)",
                            (selected_property, selected_block, selected_flat_no, amount))

        # Delete the corresponding entry from projectsavailable
        self.c.execute("DELETE FROM projectsavailable WHERE name = ? AND block = ? AND flat_no = ?",
                        (selected_property, selected_block, selected_flat_no))

        self.conn.commit()
        self.update_chart()
        # Close the windows after completing the booking
        self.destroy()

class PaymentMethodWindow(tk.Toplevel):
    def __init__(self, master, cursor, connection, username, property_name, block, flat_no, price, email, phone_no, address, aadhar_no, bank_name, amount):
        super().__init__(master)
        self.title("Payment Method")
        self.geometry("400x200")

        self.username = username
        self.property_name = property_name
        self.block = block
        self.flat_no = flat_no
        self.price = price
        self.email = email
        self.phone_no = phone_no
        self.address = address
        self.aadhar_no = aadhar_no
        self.block = block
        self.flat_no = flat_no
        self.bank_name = bank_name
        self.amount = amount

        self.method_label = ttk.Label(self, text="Select Payment Method:")
        self.method_var = StringVar()
        self.method_var.set("Cash")  # Default to Cash
        self.method_dropdown = ttk.Combobox(self, textvariable=self.method_var, values=["Cash", "NTFS"])

        self.ntfs_label = ttk.Label(self, text="Enter NTFS Number:")
        self.ntfs_entry = ttk.Entry(self)

        self.ok_button = ttk.Button(self, text="OK", command=self.complete_booking)

        self.method_label.pack(pady=10)
        self.method_dropdown.pack(pady=5)
        self.ntfs_label.pack(pady=10)
        self.ntfs_entry.pack(pady=5)
        self.ok_button.pack(pady=10)

    def complete_booking(self):
        payment_method = self.method_var.get()
        ntfs_number = self.ntfs_entry.get() if payment_method == "NTFS" else None

        # Perform the booking and payment processing here
        # You can update the database or perform any other necessary actions

        # Close the windows after completing the booking
        self.master.destroy()
        self.destroy()

class ViewPaymentDetails2Window(ThemedToplevel):
    def __init__(self, master, username, cursor, connection):
        super().__init__(master)
        self.title("View Payment Details")
        self.geometry("400x200")

        self.username = username
        self.c = cursor
        self.conn = connection

        self.view_button = ttk.Button(self, text="View Details", command=self.view_details)
        self.view_button.pack(padx=10, pady=10)

    def view_details(self):
        # Query the database for payment details of the logged-in user
        self.c.execute("SELECT paymentdet, payment_method FROM users WHERE username = ?", (self.username,))
        payment_details = self.c.fetchone()

        # Display payment details
        if payment_details:
            details_text = f"Payment Amount: {payment_details[0]}, Payment Method: {payment_details[1]}"
            messagebox.showinfo("Payment Details", f"Payment details for {self.username}:\n{details_text}")
            readn(details_text)
        else:
            messagebox.showinfo("Payment Details", f"No payment details found for {self.username}")
            readn("NO PAYMENT DETAILS")


class ProjectDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Project Details")
        self.geometry("300x100")

        self.c = cursor
        self.conn = connection

        self.update_button = ttk.Button(self, text="Update Details", command=self.open_update_window)
        self.view_button = ttk.Button(self, text="View Details", command=self.open_view_window)

        self.update_button.pack(pady=10)
        self.view_button.pack(pady=10)
    
    def open_update_window(self):
    # Ensure tables exist before opening the window
        self.create_tables_if_not_exist()
        update_project_window = UpdateProjectDetailsWindow(self, self.c, self.conn)
        update_project_window.mainloop()

    def open_view_window(self):
        # Ensure tables exist before opening the window
        self.create_tables_if_not_exist()
        view_project_window = ViewProjectDetailsWindow(self,self.c,self.conn)
        view_project_window.mainloop()

        # Run the mainloop only once for the Toplevel window
        view_project_window.mainloop()
    def create_tables_if_not_exist(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsbooked (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsavailable (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")

class UpdateProjectDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Update Project Details")
        self.geometry("400x300")

        self.c = cursor
        self.conn = connection

        self.name_label = ttk.Label(self, text="Project Name:")
        self.name_entry = ttk.Entry(self)

        self.block_label = ttk.Label(self, text="Block:")
        self.block_entry = ttk.Entry(self)

        self.flat_no_label = ttk.Label(self, text="Flat No:")
        self.flat_no_entry = ttk.Entry(self)

        self.price_label = ttk.Label(self, text="Price:")
        self.price_entry = ttk.Entry(self)

        self.update_button = ttk.Button(self, text="Update Details", command=self.update_details)

        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.block_label.grid(row=1, column=0, padx=10, pady=10)
        self.block_entry.grid(row=1, column=1, padx=10, pady=10)

        self.flat_no_label.grid(row=2, column=0, padx=10, pady=10)
        self.flat_no_entry.grid(row=2, column=1, padx=10, pady=10)

        self.price_label.grid(row=3, column=0, padx=10, pady=10)
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        self.update_button.grid(row=4, column=1, padx=10, pady=10)

    def update_details(self):
        try:
            name = self.name_entry.get()
            block = self.block_entry.get()
            flat_no = self.flat_no_entry.get()
            price = self.price_entry.get()

            self.c.execute("INSERT OR REPLACE INTO projectsavailable (name, block, flat_no, price) VALUES (?, ?, ?, ?)",
                     (name, block, flat_no, price))
            self.conn.commit()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating project details: {e}")

class ChartWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Property Chart")
        self.geometry("400x400")

        self.c = cursor
        self.conn = connection

        self.create_pie_chart()
    def update_chart(self):
        # Update the chart when called
        self.create_pie_chart()

    def create_pie_chart(self):
        # Retrieve property names and their respective booking counts from the "projectsbooked" table
        self.c.execute("SELECT name, COUNT(*) FROM projectsbooked GROUP BY name")
        property_data = self.c.fetchall()

        # Separate property names and counts
        property_names = [data[0] for data in property_data]
        booking_counts = [data[1] for data in property_data]

        # Create a pie chart using matplotlib
        labels = property_names
        sizes = booking_counts

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

        # Embed the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class ViewProjectDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("View Project Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        self.project_names = self.get_available_project_names()

        self.project_label = ttk.Label(self, text="Select Project:")
        self.project_var = StringVar(value=self.project_names[0] if self.project_names else "")
        self.project_dropdown = ttk.Combobox(self, textvariable=self.project_var, values=self.project_names)

        self.view_button = ttk.Button(self, text="View Details", command=self.view_details)
        self.show_chart_button = ttk.Button(self, text="Show Chart", command=self.show_chart)
        self.show_chart_button.grid(row=1, column=0, padx=10, pady=10)
        self.project_label.grid(row=0, column=0, padx=10, pady=10)
        self.project_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.view_button.grid(row=1, column=1, padx=10, pady=10)
    def show_chart(self):
        # Ensure tables exist before opening the window
        view_project_window = ChartWindow(self,self.c,self.conn)
        view_project_window.mainloop()

    def get_available_project_names(self):
        # Retrieve the available project names from the database
        self.c.execute("SELECT DISTINCT name FROM projectsavailable")
        projects = self.c.fetchall()
        return [project[0] for project in projects]

    def view_details(self):
        selected_project = self.project_var.get()

        # Check if a project is selected
        if not selected_project:
            messagebox.showwarning("Warning", "Please select a project.")
            return

        # Query the database for property names of the selected project
        self.c.execute("SELECT block, flat_no FROM projectsavailable WHERE name = ?", (selected_project,))
        property_details = self.c.fetchall()

        # Display property names
        if property_details:
            details_text = "\n".join([f"Block: {detail[0]}, Flat No: {detail[1]}" for detail in property_details])          # Display property details in the original window
            messagebox.showinfo("Property Details", f"Properties for {selected_project}:\n{details_text}")
        else:
            messagebox.showinfo("Property Details", f"No properties found for {selected_project}")

class PaymentDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Payment Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        self.update_button = ttk.Button(self, text="Update Details", command=self.open_update_window)
        self.view_button = ttk.Button(self, text="View Details", command=self.open_view_window)

        self.update_button.pack(pady=10)
        self.view_button.pack(pady=10)

    def open_update_window(self):
        update_payment_window = UpdatePaymentDetailsWindow(self, self.c, self.conn)
        update_payment_window.mainloop()

    def open_view_window(self):
        view_payment_window = ViewPaymentDetailsWindow(self, self.c, self.conn)
        view_payment_window.mainloop()

class UpdatePaymentDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Update Payment Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        # Get the available usernames
        self.usernames = self.get_usernames()

        self.user_label = ttk.Label(self, text="Select User:")
        self.user_var = StringVar(value=self.usernames[0] if self.usernames else "")
        self.user_dropdown = ttk.Combobox(self, textvariable=self.user_var, values=self.usernames)

        self.payment_method_label = ttk.Label(self, text="Payment Method:")
        self.payment_method_entry = ttk.Entry(self)

        self.amount_label = ttk.Label(self, text="Amount:")
        self.amount_entry = ttk.Entry(self)

        self.update_button = ttk.Button(self, text="Update Details", command=self.update_details)

        self.user_label.grid(row=0, column=0, padx=10, pady=10)
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.payment_method_label.grid(row=1, column=0, padx=10, pady=10)
        self.payment_method_entry.grid(row=1, column=1, padx=10, pady=10)

        self.amount_label.grid(row=2, column=0, padx=10, pady=10)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        self.update_button.grid(row=3, column=1, padx=10, pady=10)

    def get_usernames(self):
        # Retrieve the available usernames from the database
        self.c.execute("SELECT username FROM users")
        users = self.c.fetchall()
        return [user[0] for user in users]

    def update_details(self):
        selected_user = self.user_var.get()
        payment_method = self.payment_method_entry.get()
        amount = self.amount_entry.get()

        # Validate input
        if not amount.isdigit() or int(amount) < 0:
            messagebox.showerror("Error", "Please enter a valid positive integer amount.")
            return

        # Update the payment details in the database
        self.c.execute("INSERT OR REPLACE INTO users SET paymentdet = ?, payment_method = ? WHERE username = ?", (amount, payment_method, selected_user))
        self.conn.commit()

        # Close the window after updating details
        self.destroy()

class ViewPaymentDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("View Payment Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        # Get the available usernames
        self.usernames = self.get_usernames()

        self.user_label = ttk.Label(self, text="Select User:")
        self.user_var = StringVar(value=self.usernames[0] if self.usernames else "")
        self.user_dropdown = ttk.Combobox(self, textvariable=self.user_var, values=self.usernames)

        self.view_button = ttk.Button(self, text="View Details", command=self.view_details)

        self.user_label.grid(row=0, column=0, padx=10, pady=10)
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.view_button.grid(row=1, column=1, padx=10, pady=10)

    def get_usernames(self):
        # Retrieve the available usernames from the database
        self.c.execute("SELECT username FROM users")
        users = self.c.fetchall()
        return [user[0] for user in users]

    def view_details(self):
        selected_user = self.user_var.get()

        # Check if a user is selected
        if not selected_user:
            messagebox.showwarning("Warning", "Please select a user.")
            return

        # Query the database for payment details of the selected user
        self.c.execute("SELECT paymentdet, payment_method FROM users WHERE username = ?", (selected_user,))
        payment_details = self.c.fetchone()

        # Display payment details
        if payment_details:
            details_text = f"Payment Amount: {payment_details[0]}, Payment Method: {payment_details[1]}"
            messagebox.showinfo("Payment Details", f"Payment details for {selected_user}:\n{details_text}")
            readn(details_text)
            
        else:
            messagebox.showinfo("Payment Details", f"No payment details found for {selected_user}")
            readn("No Payment details found")
            
class BookingDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Booking Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        self.update_button = ttk.Button(self, text="Update Details", command=self.open_update_window)
        self.view_button = ttk.Button(self, text="View Details", command=self.open_view_window)

        self.update_button.pack(pady=10)
        self.view_button.pack(pady=10)

    def open_update_window(self):
        update_booking_window = UpdateBookingDetailsWindow(self, self.c, self.conn)
        update_booking_window.mainloop()

    def open_view_window(self):
        view_booking_window = ViewBookingDetailsWindow(self, self.c, self.conn)
        view_booking_window.mainloop()

class UpdateBookingDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Update Booking Details")
        self.geometry("400x400")

        self.c = cursor
        self.conn = connection

        # Get the available user names and property names
        self.user_names = self.get_user_names()
        self.property_names = self.get_property_names()

        self.user_label = ttk.Label(self, text="Select User:")
        self.user_var = StringVar(value=self.user_names[0] if self.user_names else "")
        self.user_dropdown = ttk.Combobox(self, textvariable=self.user_var, values=self.user_names)

        self.property_label = ttk.Label(self, text="Select Property:")
        self.property_var = StringVar(value=self.property_names[0] if self.property_names else "")
        self.property_dropdown = ttk.Combobox(self, textvariable=self.property_var, values=self.property_names)

        self.email_label = ttk.Label(self, text="Email:")
        self.email_entry = ttk.Entry(self)

        self.phone_label = ttk.Label(self, text="Phone No:")
        self.phone_entry = ttk.Entry(self)

        self.address_label = ttk.Label(self, text="Address:")
        self.address_entry = ttk.Entry(self)

        self.aadhar_label = ttk.Label(self, text="Aadhar No:")
        self.aadhar_entry = ttk.Entry(self)

        self.block_label = ttk.Label(self, text="Block:")
        self.block_entry = ttk.Entry(self)

        self.flat_no_label = ttk.Label(self, text="Flat No:")
        self.flat_no_entry = ttk.Entry(self)

        self.bank_name_label = ttk.Label(self, text="Bank Name:")
        self.bank_name_entry = ttk.Entry(self)

        self.amount_label = ttk.Label(self, text="Amount:")
        self.amount_entry = ttk.Entry(self)

        self.update_button = ttk.Button(self, text="Update Details", command=self.update_details)

        self.user_label.grid(row=0, column=0, padx=10, pady=10)
        self.user_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.property_label.grid(row=1, column=0, padx=10, pady=10)
        self.property_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.email_label.grid(row=2, column=0, padx=10, pady=10)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        self.phone_label.grid(row=3, column=0, padx=10, pady=10)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=10)

        self.address_label.grid(row=4, column=0, padx=10, pady=10)
        self.address_entry.grid(row=4, column=1, padx=10, pady=10)

        self.aadhar_label.grid(row=5, column=0, padx=10, pady=10)
        self.aadhar_entry.grid(row=5, column=1, padx=10, pady=10)

        self.block_label.grid(row=6, column=0, padx=10, pady=10)
        self.block_entry.grid(row=6, column=1, padx=10, pady=10)

        self.flat_no_label.grid(row=7, column=0, padx=10, pady=10)
        self.flat_no_entry.grid(row=7, column=1, padx=10, pady=10)

        self.bank_name_label.grid(row=8, column=0, padx=10, pady=10)
        self.bank_name_entry.grid(row=8, column=1, padx=10, pady=10)

        self.amount_label.grid(row=9, column=0, padx=10, pady=10)
        self.amount_entry.grid(row=9, column=1, padx=10, pady=10)

        self.update_button.grid(row=10, column=1, padx=10, pady=10)

    def get_user_names(self):
        # Retrieve the available customer names from the database
        self.c.execute("SELECT DISTINCT customer_name FROM bookingdetails")
        customers = self.c.fetchall()
        return [customer[0] for customer in customers]

    def get_property_names(self):
        # Retrieve the available property names from the database
        self.c.execute("SELECT DISTINCT property_name FROM bookingdetails")
        properties = self.c.fetchall()
        return [property[0] for property in properties]

    def update_details(self):
        selected_user = self.user_var.get()
        selected_property = self.property_var.get()
        email = self.email_entry.get()
        phone_no = self.phone_entry.get()
        address = self.address_entry.get()
        aadhar_no = self.aadhar_entry.get()
        block = self.block_entry.get()
        flat_no = self.flat_no_entry.get()
        bank_name = self.bank_name_entry.get()
        amount = self.amount_entry.get()

                # Check if the entry already exists in projectsbooked
        self.c.execute("SELECT * FROM projectsbooked WHERE name = ? AND block = ? AND flat_no = ?",
                    (selected_property, block, flat_no))
        existing_entry = self.c.fetchone()

        if existing_entry:
            # Entry exists, perform update
            self.c.execute("UPDATE projectsbooked SET price = ? WHERE name = ? AND block = ? AND flat_no = ?",
                        (amount, selected_property, block, flat_no))
        else:
            # Entry doesn't exist, perform insert
            self.c.execute("INSERT INTO projectsbooked (name, block, flat_no, price) VALUES (?, ?, ?, ?)",
                        (selected_property, block, flat_no, amount))

            # Delete the corresponding entry from projectsavailable
            self.c.execute("DELETE FROM projectsavailable WHERE name = ? AND block = ? AND flat_no = ?",
                        (selected_property, block, flat_no))

        # Continue with the rest of the code
        self.c.execute("INSERT OR REPLACE INTO bookingdetails (customer_name, email, phone_no, address, aadhar_no, property_name, block_name, flat_no, bank_name, amount) "
                    "SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ? FROM users JOIN projectsavailable ON users.username = ? AND projectsavailable.name = ?",
                    (selected_user, email, phone_no, address, aadhar_no, selected_property, block, flat_no, bank_name, amount, selected_user, selected_property))

        self.conn.commit()

        # Close the window after updating details
        self.destroy()

class ViewBookingDetailsWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("View Booking Details")
        self.geometry("400x200")

        self.c = cursor
        self.conn = connection

        # Get the available customer names and property names
        self.customer_names = self.get_customer_names()
        self.property_names = self.get_property_names()

        self.customer_label = ttk.Label(self, text="Select Customer:")
        self.customer_var = StringVar(value=self.customer_names[0] if self.customer_names else "")
        self.customer_dropdown = ttk.Combobox(self, textvariable=self.customer_var, values=self.customer_names)

        self.property_label = ttk.Label(self, text="Select Property:")
        self.property_var = StringVar(value=self.property_names[0] if self.property_names else "")
        self.property_dropdown = ttk.Combobox(self, textvariable=self.property_var, values=self.property_names)

        self.view_button = ttk.Button(self, text="View Details", command=self.view_details)

        self.customer_label.grid(row=0, column=0, padx=10, pady=10)
        self.customer_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.property_label.grid(row=1, column=0, padx=10, pady=10)
        self.property_dropdown.grid(row=1, column=1, padx=10, pady=10)

        self.view_button.grid(row=2, column=1, padx=10, pady=10)

    def get_customer_names(self):
    # Retrieve unique customer names from the bookingdetails table
        self.c.execute("SELECT DISTINCT customer_name FROM bookingdetails")
        customers = self.c.fetchall()
        return [customer[0] for customer in customers]

    def get_property_names(self):
        # Retrieve unique property names from the bookingdetails table
        self.c.execute("SELECT DISTINCT property_name FROM bookingdetails")
        properties = self.c.fetchall()
        return [property[0] for property in properties]


    def view_details(self):
        selected_customer = self.customer_var.get()
        selected_property = self.property_var.get()

        # Validate input if needed

        # Query the database for booking details of the selected customer and property
        self.c.execute("SELECT * FROM bookingdetails WHERE customer_name = ? AND property_name = ?", (selected_customer, selected_property))
        booking_details = self.c.fetchone()

        # Display booking details
        if booking_details:
            field_names = ["Customer", "Email", "Phone No", "Address", "Aadhar No", "Property", "Block", "Flat No", "Bank Name", "Amount"]
            details_text = ", ".join([f"{field}: {value}" for field, value in zip(field_names, booking_details)])
            messagebox.showinfo("Booking Details", f"Booking details for {selected_customer} and {selected_property}:\n{details_text}")
            readn(details_text)
        else:
            messagebox.showinfo("Booking Details", f"No booking details found for {selected_customer} and {selected_property}")
            readn("No Booking details found")

class LoginWindow(ThemedToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Login")

        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate quarter of the screen width and height
        quarter_width = screen_width // 4
        quarter_height = screen_height // 4

        # Calculate the center position
        center_x = (screen_width - quarter_width) // 2
        center_y = (screen_height - quarter_height) // 2

        self.geometry(f"{quarter_width}x{quarter_height}+{center_x}+{center_y}")
        self.columnconfigure(0, weight=1)  # Ensure center alignment
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.load_image()

        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_entry = ttk.Entry(self, show="*")

        self.login_button = ttk.Button(self, text="Login", command=self.login)
        self.forgot_password_button = ttk.Button(self, text="Forgot Password?", command=self.open_forgot_password_window)
        self.create_account_button = ttk.Button(self, text="Create Account", command=self.open_create_account_window)

        self.username_label.grid(row=0, column=0, pady=(15, 5), padx=(10, 0), sticky="w")  # Adjusted position
        self.username_entry.grid(row=0, column=1, pady=(15, 5), sticky="w")

        self.password_label.grid(row=1, column=0, pady=5, padx=(10, 0), sticky="w")  # Adjusted position
        self.password_entry.grid(row=1, column=1, pady=5, sticky="w")

        # Adjusted button positioning and sizes
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")
        self.forgot_password_button.grid(row=3, column=0, pady=10, padx=5, sticky="nsew")
        self.create_account_button.grid(row=3, column=1, pady=10, padx=5, sticky="nsew")

        self.conn = sqlite3.connect("C:\\ZZZZ-MINE\\Manipal\\Semester 5\\sqlite-tools-win32-x86-3430200\\my databases\\testDB.sqlite3")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT DEFAULT 'customer', paymentdet TEXT, payment_method TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsbooked (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")
        self.c.execute("CREATE TABLE IF NOT EXISTS projectsavailable (name TEXT, block TEXT, flat_no TEXT, price INTEGER, PRIMARY KEY (name, block, flat_no))")
        self.c.execute("CREATE TABLE IF NOT EXISTS bookingdetails (customer_name TEXT, email TEXT, phone_no TEXT, address TEXT, aadhar_no TEXT, property_name TEXT, block_name TEXT, flat_no TEXT, bank_name TEXT, amount INTEGER, PRIMARY KEY (customer_name, property_name, block_name, flat_no))")
    def load_image(self):
        img_path = "C:\\ZZZZ-MINE\\Manipal\\Semester 5\\AP\\startbootstrap-sb-admin-2-gh-pages\\ap\\download.jpg"
        img = Image.open(img_path)
        img = img.resize((100, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)

        self.image_label = ttk.Label(self, image=img, borderwidth=0)
        self.image_label.image = img

        # Integrated photo with the background
        self.image_label.grid(row=0, column=2, rowspan=4, padx=10, pady=10, sticky="e")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.c.fetchone()

        if user is None:
            messagebox.showerror("Error", "Invalid username or password.")
        elif len(user) < 3 or user[1] != password:
            messagebox.showerror("Error", "Invalid username or password.")
        else:
            self.open_dashboard(username, user[2])  # Pass the user's role as the third element

    def open_dashboard(self, username, role):
        if role == "admin":
            admin_dashboard = AdminDashboard(self, username, self.c, self.conn)
            admin_dashboard.mainloop()
        elif role == "customer":
            customer_dashboard = CustomerDashboard(self, username, self.c, self.conn)
            customer_dashboard.mainloop()


    def open_forgot_password_window(self):
        forgot_password_window = ForgotPasswordWindow(self, self.c, self.conn)
        forgot_password_window.mainloop()

    def open_create_account_window(self):
        create_account_window = CreateAccountWindow(self, self.c, self.conn)
        create_account_window.mainloop()

    def destroy(self):
        self.c.close()
        self.conn.close()
        super().destroy()

class CreateAccountWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Create Account")
        self.geometry("400x250")  # Quarter-page geometry
        
        self.c=cursor
        self.conn=connection
        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)

        self.password_label = ttk.Label(self, text="Password:")
        self.password_entry = ttk.Entry(self, show="*")

        self.role_label = ttk.Label(self, text="Select Role:")
        self.role_var = tk.StringVar(value="admin")  # Default role is admin
        self.admin_radio = ttk.Radiobutton(self, text="Admin", variable=self.role_var, value="admin")
        self.customer_radio = ttk.Radiobutton(self, text="Customer", variable=self.role_var, value="customer")
        self.create_account_button = ttk.Button(self, text="Create Account", command=self.create_account)

        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.role_label.grid(row=2, column=0, padx=10, pady=10)
        self.admin_radio.grid(row=2, column=1, padx=10, pady=10)
        self.customer_radio.grid(row=2, column=2, padx=10, pady=10)
        self.create_account_button.grid(row=3, column=0, columnspan=2, pady=10)

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()

        # Check role-specific username length requirements
        if (role == "admin" and len(username) != 5) or (role == "customer" and len(username) != 8):
            messagebox.showerror("Error", f"Invalid username length for {role} account.")
        else:
            self.c.execute("SELECT * FROM users WHERE username = ?", (username,))

            user = self.c.fetchone()

            if user is not None:
                messagebox.showerror("Error", "Username already exists.")
            else:
                self.c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
                self.conn.commit()

                messagebox.showinfo("Success", "Account created successfully.")

                self.destroy()

class ForgotPasswordWindow(ThemedToplevel):
    def __init__(self, master, cursor, connection):
        super().__init__(master)
        self.title("Forgot Password")
        self.geometry("400x250")  # Quarter-page geometry
        self.c = cursor
        self.conn = connection

        self.step = 1  # Track the current step

        self.username_label = ttk.Label(self, text="Username:")
        self.username_entry = ttk.Entry(self)
        self.next_button = ttk.Button(self, text="Next", command=self.next_step)

        self.new_password_label = ttk.Label(self, text="New Password:")
        self.new_password_entry = ttk.Entry(self, show="*")
        self.reset_password_button = ttk.Button(self, text="Reset Password", command=self.reset_password)

        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.next_button.grid(row=1, column=1, padx=10, pady=10)

        # Adjust the button positioning and size
        button_width = 15
        button_height = 2

        self.next_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.reset_password_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

    def next_step(self):
        if self.step == 1:
            username = self.username_entry.get()

            self.c.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = self.c.fetchone()

            if user is None:
                messagebox.showerror("Error", "Invalid username.")
            else:
                self.step = 2
                self.username_entry.config(state="disabled")  # Disable username entry
                self.new_password_label.grid(row=2, column=0, padx=10, pady=10)
                self.new_password_entry.grid(row=2, column=1, padx=10, pady=10)
                self.reset_password_button.grid(row=3, column=1, padx=10, pady=10)
        else:
            messagebox.showerror("Error", "Invalid step.")

    def reset_password(self):
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()

        self.c.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        self.conn.commit()

        messagebox.showinfo("Success", "Password reset successfully.")

        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("REAL ESTATE MANAGEMENT SYSTEM")
    login_window = LoginWindow(root)
    root.mainloop()