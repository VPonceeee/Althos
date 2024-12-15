import tkinter as tk
from tkinter import StringVar
from pymongo import MongoClient

class SignUpForm(tk.Tk):
    def __init__(self, parent_form=None):
        super().__init__()
        self.parent_form = parent_form  # Reference to the parent LoginForm

        # Database Connection
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            self.client = MongoClient(connection_string)
            print("Connected to MongoDB Atlas!")
            
            # Accessing the database and collection
            self.db = self.client["ADB"]  # Database name
            self.accounts_collection = self.db["Accounts"]  # Collection name
            
        except Exception as e:
            print("Error connecting to MongoDB:", e)
            return

        # Form Section
        self.title("ALTHOS")
        Formwidth, Formheight = 400, 500
        self.geometry(f"{Formwidth}x{Formheight}")
        self.resizable(False, False)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - Formwidth) // 2
        y = (screen_height - Formheight) // 2
        self.geometry(f"{Formwidth}x{Formheight}+{x}+{y}")
        self.overrideredirect(True)

        # Top Panel Section ---------------------------------------------------------------------
        self.top_panel = tk.Frame(self, height=90)
        self.top_panel.pack(side="top", fill="x")

        self.SystemName_lbl = tk.Label(self.top_panel, text="Sign Up", font=("Arial", 20, "bold"), fg="green")
        self.SystemName_lbl.pack(side="top", fill="both", padx=1, pady=15)

        # Info Panel Section ---------------------------------------------------------------------
        self.Info_panel = tk.Frame(self, height=150)
        self.Info_panel.pack(side="top", fill="x", padx=(25, 25))

        # Show Password and Status Message Panel Section ---------------------------------------------------------------------
        self.InfoBottom_pnl = tk.Frame(self, height=40)
        self.InfoBottom_pnl.pack(side="top", fill="x", padx=(25, 25))
        self.InfoBottom_pnl.pack_propagate(False)

        # Buttons Panel Section ---------------------------------------------------------------------
        self.btn_pnl = tk.Frame(self, height=110)
        self.btn_pnl.pack(side="top", fill="x", padx=(25, 25))
        self.btn_pnl.pack_propagate(False)

        # Username Label and Entry
        self.Username_lbl = tk.Label(self.Info_panel, text="Username:", font=("Arial", 10, "bold"))
        self.Username_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Username_txtb = tk.Entry(self.Info_panel, font=("Arial", 14), width=40)
        self.Username_txtb.pack(anchor="w", padx=1, pady=1)

        # Email Label and Entry
        self.Email_lbl = tk.Label(self.Info_panel, text="Email:", font=("Arial", 10, "bold"))
        self.Email_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Email_txtb = tk.Entry(self.Info_panel, font=("Arial", 14), width=40)
        self.Email_txtb.pack(anchor="w", padx=1, pady=1)

        # Password Label and Entry
        self.Pass_lbl = tk.Label(self.Info_panel, text="Password:", font=("Arial", 10, "bold"))
        self.Pass_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.password_var = StringVar()
        self.Pass_txtb = tk.Entry(self.Info_panel, textvariable=self.password_var, font=("Arial", 14), show="*", width=40)
        self.Pass_txtb.pack(anchor="w", padx=1, pady=1)

        # Confirm Password Label and Entry
        self.CPass_lbl = tk.Label(self.Info_panel, text="Confirm Password:", font=("Arial", 10, "bold"))
        self.CPass_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.confirm_password_var = StringVar()
        self.CPass_txtb = tk.Entry(self.Info_panel, textvariable=self.confirm_password_var, font=("Arial", 14), show="*", width=40)
        self.CPass_txtb.pack(anchor="w", padx=1, pady=1)

        # Show Password Checkbox
        self.show_password_var = tk.BooleanVar()
        self.ShowPass_cb = tk.Checkbutton(self.InfoBottom_pnl, text="Show Password", font=("Arial", 10), variable=self.show_password_var, command=self.toggle_password_visibility)
        self.ShowPass_cb.pack(side="left", padx=(1,1), pady=(10,10))

        #Status Message
        self.Status_lbl = tk.Label(self.InfoBottom_pnl, text="", font=("Arial", 10), fg="red")
        self.Status_lbl.pack(side="right", padx=(5,5), pady=(10,10))

        # Sign-Up Button
        self.SignUp_btn = tk.Button(self.btn_pnl, text="Sign Up", bg="green", fg="white", height=2, width=50, relief="flat", command=self.AddData)
        self.SignUp_btn.pack(anchor="w", padx=1, pady=(10, 7))

        # Cancel Button
        self.Cancel_btn = tk.Button(self.btn_pnl, text="Cancel", bg="darkred", fg="white", height=2, width=50, relief="flat", command=self.BackToLogin)
        self.Cancel_btn.pack(anchor="w", padx=1, pady=1)

    def toggle_password_visibility(self):
        # Toggle between hidden and visible passwords
        if self.show_password_var.get():
            self.Pass_txtb.config(show="")
            self.CPass_txtb.config(show="")
        else:
            self.Pass_txtb.config(show="*")
            self.CPass_txtb.config(show="*")

    def AddData(self):
        # Retrieve values from input fields
        username = self.Username_txtb.get().strip()
        email = self.Email_txtb.get().strip()
        password = self.password_var.get().strip()
        confirm_password = self.confirm_password_var.get().strip()

        # Validation checks
        if not username or not email or not password or not confirm_password:
            print("All fields are required!")
            self.Status_lbl.config(text="All fields are required!", fg="red")
            return
        
        if password != confirm_password:
            print("Passwords do not match!")
            self.Status_lbl.config(text="Passwords do not match!", fg="red")
            return

        # Insert data into MongoDB
        try:
            user_data = {
                "username": username,
                "email": email,
                "password": password  # Use hashing in production!
            }
            self.accounts_collection.insert_one(user_data)
            print("User registered successfully!")
            self.Status_lbl.config(text="Account created successfully!", fg="green")

            # Clear fields after success
            self.Username_txtb.delete(0, 'end')
            self.Email_txtb.delete(0, 'end')
            self.Pass_txtb.delete(0, 'end')
            self.CPass_txtb.delete(0, 'end')
            self.Status_lbl.config(text="", fg="green")
            self.BackToLogin()
        
        except Exception as e:
            print(f"Error saving to database: {e}")

    def BackToLogin(self):
        self.destroy()
        if self.parent_form:
            self.parent_form.__init__()
            self.parent_form.mainloop()