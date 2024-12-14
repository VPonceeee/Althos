import tkinter as tk
from pymongo import MongoClient
from SignUp_Form import SignUpForm
from MainPage_Form import MainPage


class LoginForm(tk.Tk):
    def __init__(self): 
        super().__init__()

        # Database Connection ---------------------------------------------------------------------
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            self.client = MongoClient(connection_string)
            self.db = self.client["ADB"]
            self.accounts_collection = self.db["Accounts"] 
            print("Connected to MongoDB Atlas!")
        except Exception as e:
            print("Error connecting to MongoDB:", e)

        # Form Section ---------------------------------------------------------------------
        self.title("ALTHOS")  
        Formwidth, Formheight = 400, 500 
        self.geometry(f"{Formwidth}x{Formheight}") 
        self.resizable(False, False)  
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight() 
        x = (screen_width - Formwidth) // 2 
        y = (screen_height - Formheight) // 2  
        self.geometry(f"{Formwidth}x{Formheight}+{x}+{y}") 

        # Top Panel Section ---------------------------------------------------------------------
        self.top_panel = tk.Frame(self, height=120) 
        self.top_panel.pack(side="top", fill="x")

        # Label system name
        self.SystemName_lbl = tk.Label(self.top_panel, text="", font=("Arial", 30, "bold"), fg="green")
        self.SystemName_lbl.pack(side="top", fill="both", padx=1, pady=45)
        self.SystemName_lbl.config(text=f"ALTHOS")

        # Info Panel Section ---------------------------------------------------------------------
        self.Info_panel = tk.Frame(self, height=200) 
        self.Info_panel.pack(side="top", fill="x", padx=(25, 25))

        # Email Label
        self.Email_lbl = tk.Label(self.Info_panel, text="", font=("Arial", 10, "bold")) 
        self.Email_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Email_lbl.config(text=f"Email:")

        # Email Textbox
        self.Email_txtb = tk.Text(self.Info_panel, height=1, width=40, font=("Arial", 14))
        self.Email_txtb.pack(anchor="w", padx=1, pady=1)

        # Password Label
        self.Pass_lbl = tk.Label(self.Info_panel, text="", font=("Arial", 10, "bold")) 
        self.Pass_lbl.pack(side="top", anchor="w", padx=1, pady=(10, 2))
        self.Pass_lbl.config(text=f"Password:")

        # Password Textbox
        self.Pass_txtb = tk.Entry(self.Info_panel, width=40, font=("Arial", 14), show="*")
        self.Pass_txtb.pack(anchor="w", padx=1, pady=1)

        # Show Password Checkbox
        self.ShowPass_cb = tk.Checkbutton(self.Info_panel, text="Show Password", font=("Arial", 10), command=self.ShowPassword)
        self.ShowPass_cb.pack(anchor="w", padx=1, pady=1)

        # Login Button
        self.Login_btn = tk.Button(self.Info_panel, text="Login", bg="green", fg="white", height=2, width=50, relief="flat", command=self.ReadData)
        self.Login_btn.pack(anchor="w", padx=1, pady=(10, 7))

        # SignUp Button
        self.SignUp_btn = tk.Button(self.Info_panel, text="Sign Up", bg="green", fg="white", height=2, width=50, relief="flat", command=self.ShowSignUpForm)
        self.SignUp_btn.pack(anchor="w", padx=1, pady=1)


#FUNCTION AND CONDITION SECTION ----------------------------------------------------------------------------------------------------------------

    def ShowPassword(self):
        if self.Pass_txtb.cget('show') == '*':
            self.Pass_txtb.config(show='')
        else:
            self.Pass_txtb.config(show='*')

    def ReadData(self):
        email = self.Email_txtb.get("1.0", "end").strip()
        password = self.Pass_txtb.get().strip()

        if not email or not password:
            print("Please fill out both fields!")
            return

        try:
            user = self.accounts_collection.find_one({"email": email, "password": password})
            
            if user:
                print("Login successful! Welcome,", user["username"])
                self.destroy() 
                MainPageForm = MainPage(user["username"], user["_id"]) 
                MainPageForm.mainloop()
            else:
                print("Invalid email or password! Please try again.")

        except Exception as e:
            print("Error querying the database:", e)

    def ShowSignUpForm(self):
        self.destroy() 
        signup_form = SignUpForm(self)
        signup_form.mainloop()


# Start the Tkinter event loop
if __name__ == "__main__":  
    app = LoginForm()  
    app.mainloop()
