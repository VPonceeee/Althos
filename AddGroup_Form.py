import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId

class AddGroups(tk.Toplevel):
    def __init__(self, parent, AccID):
        super().__init__(parent)

        #Get the Value
        self.AccID = AccID 

        # Database Connection Section ---------------------------------------------------------------------
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            self.client = MongoClient(connection_string)
            self.db = self.client["ADB"]
            self.groups_collection = self.db["Groups"]
            print("Connected to MongoDB Atlas!")
        except Exception as e:
            print("Error connecting to MongoDB:", e)

        #Form Properties Section ---------------------------------------------------------------------
        self.title("Add Groups")  
        Formwidth, Formheight = 500, 130 
        self.geometry(f"{Formwidth}x{Formheight}") 
        self.resizable(False, False)  
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight() 
        x = (screen_width - Formwidth) // 2 
        y = (screen_height - Formheight) // 2  
        self.geometry(f"{Formwidth}x{Formheight}+{x}+{y}")
        self.grab_set()
        self.attributes('-topmost', 1)
        
        # Top and Bottom Panel Section ---------------------------------------------------------------------
        self.top_panel = tk.Frame(self, height=100) 
        self.top_panel.pack(side="top", fill="x")

        self.bottom_panel = tk.Frame(self, height=30) 
        self.bottom_panel.pack(side="bottom", fill="x")

        self.TopLeft_panel = tk.Frame(self.top_panel, height=60, width=300) 
        self.TopLeft_panel.pack(side="left", fill="both", padx=(10,10), pady=(10,10))

        self.BottomRight_panel1 = tk.Frame(self.bottom_panel, height=30, width=80) 
        self.BottomRight_panel1.pack(side="right", fill="both", padx=(5,10), pady=(5,5))

        self.BottomRight_panel2 = tk.Frame(self.bottom_panel, height=30, width=80) 
        self.BottomRight_panel2.pack(side="right", fill="both", padx=(5,5), pady=(5,5))


        #Add Group Name Label ---------------------------------------------------------------------
        self.GroupName_lbl = tk.Label(self.TopLeft_panel, text="", font=("Arial", 12), fg="Black")
        self.GroupName_lbl.pack(anchor="w")
        self.GroupName_lbl.config(text=f"Enter Group Name:")

        # Group Name Textbox
        self.GroupName_txtb = tk.Text(self.TopLeft_panel, height=1, width=50, font=("Arial", 14))
        self.GroupName_txtb.pack(anchor="w", padx=1, pady=(10,5))

        #Add Group Button
        self.Add_btn = tk.Button(self.BottomRight_panel1, text="Add", bg="green", fg="white", height=1, width=10, relief="flat",command=self.AddData)
        self.Add_btn.pack(anchor="w", padx=1, pady=1)

        #Cancel Button
        self.Cancel_btn = tk.Button(self.BottomRight_panel2, text="Cancel", bg="darkred", fg="white", height=1, width=10, relief="flat", command=self.destroy)
        self.Cancel_btn.pack(anchor="w", padx=1, pady=1)


#FUNCTIONS AND CONDITIONS SECTION ---------------------------------------------------------------------

    def AddData(self):
        group_name = self.GroupName_txtb.get("1.0", "end").strip()

        if not group_name:
            print("Group Name cannot be empty!")
            return

        group_data = {
            "GroupName": group_name,
            "CreatedBy": ObjectId(self.AccID) 
        }

        try:
            result = self.groups_collection.insert_one(group_data)
            print(f"Group added successfully with ID: {result.inserted_id}")
            self.destroy()
        except Exception as e:
            print(f"Error inserting group data: {e}")


