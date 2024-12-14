import tkinter as tk
from DashboardPage import Dashboard  # Assuming Dashboard is a frame-based class

class MainPage(tk.Tk):
    def __init__(self,username,AccID):
        super().__init__()

        # Form Section ---------------------------------------------------------------------
        self.title("ALTHOS Dashboard")  
        form_width, form_height = 800, 600  
        self.geometry(f"{form_width}x{form_height}") 
        self.minsize(form_width, form_height) 

        # Center the form on the screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - form_width) // 2
        y = (screen_height - form_height) // 2
        self.geometry(f"{form_width}x{form_height}+{x}+{y}")

        # Left and Right Panel Section ---------------------------------------------------------------------
        self.left_panel = tk.Frame(self, width=30) 
        self.left_panel.pack(side="left", fill="y")

        #self.right_panel = tk.Frame(self, width=10, bg="black") 
        #self.right_panel.pack(side="right", fill="y")

        # Top and Bottom Panel Section ---------------------------------------------------------------------
        self.top_panel = tk.Frame(self, height=80) 
        self.top_panel.pack(side="top", fill="x")

        self.bottom_panel = tk.Frame(self, height=50) 
        self.bottom_panel.pack(side="bottom", fill="x")

        # Center Panel Section ---------------------------------------------------------------------
        self.center_panel = tk.Frame(self, bg="white")  # Background to see the panel clearly
        self.center_panel.pack(side="top", fill="both", expand=True)

        # Panel for page name ---------------------------------------------------------------------
        self.TopLeft_panel = tk.Frame(self.top_panel, height=60, width=300) 
        self.TopLeft_panel.pack(side="left", fill="both", padx=(10,10), pady=(10,10))

        self.TopRight_panel = tk.Frame(self.top_panel, height=60, width=300) 
        self.TopRight_panel.pack(side="right", fill="both", padx=(10,10), pady=(10,10))

        # Page Label ---------------------------------------------------------------------
        self.PageName_lbl = tk.Label(self.TopLeft_panel, text="", font=("Arial", 18, "bold"), fg="Black")
        self.PageName_lbl.pack(anchor="w")
        self.PageName_lbl.config(text=f"Dashboard")

        self.username = username
        self.AccID = AccID

        self.Username_lbl = tk.Label(self.TopRight_panel, text="", font=("Arial", 12, "bold"), fg="Black")
        self.Username_lbl.pack(anchor="e")
        self.Username_lbl.config(text=f"{self.username}")

        self.UserID_lbl = tk.Label(self.TopRight_panel, text="", font=("Arial", 12, "bold"), fg="Black")
        self.UserID_lbl.pack(anchor="e")
        self.UserID_lbl.config(text=f"{self.AccID}")
        
        # Load the Dashboard
        self.ShowDashboard()  # Corrected to call the method properly

    # Function and condition section -----------------------------------------------------------------------------------
    def ShowDashboard(self): 
        # Clear any existing widgets in the center panel
        for widget in self.center_panel.winfo_children():  
            widget.destroy()  

        # Create and display the Dashboard inside the center panel
        ShowDashboard = Dashboard(self.center_panel, self.username, self.AccID) 
        ShowDashboard.pack(fill=tk.BOTH, expand=True)


