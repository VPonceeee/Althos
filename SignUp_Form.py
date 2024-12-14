import tkinter as tk
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
        self.Info_panel = tk.Frame(self, height=200)
        self.Info_panel.pack(side="top", fill="x", padx=(25, 25))

        # Username Label and Textbox
        self.Username_lbl = tk.Label(self.Info_panel, text="Username:", font=("Arial", 10, "bold"))
        self.Username_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Username_txtb = tk.Text(self.Info_panel, height=1, width=40, font=("Arial", 14))
        self.Username_txtb.pack(anchor="w", padx=1, pady=1)

        # Email Label and Textbox
        self.Email_lbl = tk.Label(self.Info_panel, text="Email:", font=("Arial", 10, "bold"))
        self.Email_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Email_txtb = tk.Text(self.Info_panel, height=1, width=40, font=("Arial", 14))
        self.Email_txtb.pack(anchor="w", padx=1, pady=1)

        # Password Label and Textbox
        self.Pass_lbl = tk.Label(self.Info_panel, text="Password:", font=("Arial", 10, "bold"))
        self.Pass_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Pass_txtb = tk.Text(self.Info_panel, height=1, width=40, font=("Arial", 14))
        self.Pass_txtb.pack(anchor="w", padx=1, pady=1)

        # Confirm Password Label and Textbox
        self.CPass_lbl = tk.Label(self.Info_panel, text="Confirm Password:", font=("Arial", 10, "bold"))
        self.CPass_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.CPass_txtb = tk.Text(self.Info_panel, height=1, width=40, font=("Arial", 14))
        self.CPass_txtb.pack(anchor="w", padx=1, pady=1)

        # Show Password Checkbox
        self.ShowPass_cb = tk.Checkbutton(self.Info_panel, text="Show Password", font=("Arial", 10))
        self.ShowPass_cb.pack(anchor="w", padx=1, pady=1)

        # Sign-Up Button
        self.SignUp_btn = tk.Button(self.Info_panel, text="Sign Up", bg="green", fg="white", height=2, width=50, relief="flat", command=self.AddData)
        self.SignUp_btn.pack(anchor="w", padx=1, pady=(10, 7))

        # Cancel Button
        self.Cancel_btn = tk.Button(self.Info_panel, text="Cancel", bg="darkred", fg="white", height=2, width=50, relief="flat", command=self.BackToLogin)
        self.Cancel_btn.pack(anchor="w", padx=1, pady=1)

    def AddData(self):
        # Retrieve values from input fields
        username = self.Username_txtb.get("1.0", "end").strip()
        email = self.Email_txtb.get("1.0", "end").strip()
        password = self.Pass_txtb.get("1.0", "end").strip()
        confirm_password = self.CPass_txtb.get("1.0", "end").strip()

        # Validation checks
        if not username or not email or not password or not confirm_password:
            print("All fields are required!")
            return
        
        if password != confirm_password:
            print("Passwords do not match!")
            return

        # Insert data into MongoDB
        try:
            user_data = {
                "username": username,
                "email": email,
                "password": password  # Use hashing in production!
            }

            # Insert into the Accounts collection
            self.accounts_collection.insert_one(user_data)
            print("User registered successfully!")

            # Clear fields after success
            self.Username_txtb.delete("1.0", "end")
            self.Email_txtb.delete("1.0", "end")
            self.Pass_txtb.delete("1.0", "end")
            self.CPass_txtb.delete("1.0", "end")

            #Back to the login page
            self.destroy()
            if self.parent_form:
                self.parent_form.__init__()
                self.parent_form.mainloop()

        except Exception as e:
            print(f"Error saving to database: {e}")

    def BackToLogin(self):
        self.destroy()
        if self.parent_form:
            self.parent_form.__init__()
            self.parent_form.mainloop()


