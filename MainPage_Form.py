import tkinter as tk
from DashboardPage import Dashboard  
from ViewGroup_Form import ViewGroup

class MainPage(tk.Tk):
    def __init__(self,username,AccID):
        super().__init__()

        # Form Section ---------------------------------------------------------------------
        self.title("ALTHOS Dashboard")  
        self.state('zoomed')
        form_width, form_height = 800, 600  
        self.geometry(f"{form_width}x{form_height}") 
        self.minsize(800, 600) 

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
        self.center_panel = tk.Frame(self, bg="white") 
        self.center_panel.pack(side="top", fill="both", expand=True)

        # Panel for page name ---------------------------------------------------------------------
        self.TopLeft_panel = tk.Frame(self.top_panel, height=60, width=400) 
        self.TopLeft_panel.pack(side="left", fill="both", padx=(10,10), pady=(10,10))

        # Panel for Back Button
        self.BackBtn_pnl = tk.Frame(self.TopLeft_panel)
        self.BackBtn_pnl.pack(side="left", fill="both", expand=True,  padx=(5,5))

        # Back Button
        self.Back_btn = tk.Button(self.BackBtn_pnl, text="←", font=("Arial", 10, "bold"), command=self.ShowDashboard, relief="flat", fg="Black")
        self.Back_btn.pack(side="left")
        self.Back_btn.pack_forget() 

        self.TopRight_panel = tk.Frame(self.top_panel, height=60, width=300) 
        self.TopRight_panel.pack(side="right", fill="both", padx=(10,10), pady=(10,10))

        # Page Label ---------------------------------------------------------------------
        self.PageName_lbl = tk.Label(self.TopLeft_panel, text="", font=("Arial", 18, "bold"), fg="Black")
        self.PageName_lbl.pack(anchor="w", pady=(10,10))
     
        self.username = username
        self.AccID = AccID

        self.Username_lbl = tk.Label(self.TopRight_panel, text="", font=("Arial", 12, "bold"), fg="Black")
        self.Username_lbl.pack(anchor="e")
        self.Username_lbl.config(text=f"{self.username}")

        self.UserID_lbl = tk.Label(self.TopRight_panel, text="", font=("Arial", 12, "bold"), fg="Black")
        self.UserID_lbl.pack(anchor="e")
        self.UserID_lbl.config(text=f"{self.AccID}")
        
        # Load the Dashboard
        self.ShowDashboard() 

    # Function and condition section -----------------------------------------------------------------------------------

    #Show the Dashboard page
    def ShowDashboard(self): 
        for widget in self.center_panel.winfo_children():  
            widget.destroy()  

        ShowDashboard = Dashboard(self.center_panel, self.username, self.AccID,self.ShowViewGroup) 
        ShowDashboard.pack(fill=tk.BOTH, expand=True)
        self.PageName_lbl.config(text="Dashboard")
        self.Back_btn.pack_forget()

    #Show the View Group page
    def ShowViewGroup(self, group_name, group_id):
        for widget in self.center_panel.winfo_children():
            widget.destroy()

        view_group = ViewGroup(self.center_panel, group_name,group_id)
        view_group.pack(fill=tk.BOTH, expand=True)
        
        # Update the label to display both group_name and group_id
        self.PageName_lbl.config(text=f"{group_name}")
        self.Back_btn.pack(side="left")
        



