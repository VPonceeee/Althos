import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId

class AddMembers(tk.Toplevel):
    def __init__(self, parent, group_id):
        super().__init__(parent)

        #Get the Value
        self.group_id = group_id
        # Database Connection Section ---------------------------------------------------------------------
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            self.client = MongoClient(connection_string)
            self.db = self.client["ADB"]  # Replace with your database name
            self.members_collection = self.db["Members"]  # Replace with your collection name
            print("Connected to MongoDB!")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.destroy()
            return

        #Form Properties Section ---------------------------------------------------------------------
        self.title("Add Member")  
        Formwidth, Formheight = 500, 200 
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


        #Add Member Name Label ---------------------------------------------------------------------
        self.MemberName_lbl = tk.Label(self.TopLeft_panel, text="", font=("Arial", 12), fg="Black")
        self.MemberName_lbl.pack(anchor="w")
        self.MemberName_lbl.config(text=f"Member Name:")

        # Member Name Textbox
        self.MemberName_txtb = tk.Text(self.TopLeft_panel, height=1, width=50, font=("Arial", 14))
        self.MemberName_txtb.pack(anchor="w", padx=1, pady=(10,10))

        #Add Member IP Label ---------------------------------------------------------------------
        self.MemberIP_lbl = tk.Label(self.TopLeft_panel, text="", font=("Arial", 12), fg="Black")
        self.MemberIP_lbl.pack(anchor="w")
        self.MemberIP_lbl.config(text=f"Member IP Address:")

        # Member IP Textbox
        self.MemberIP_txtb = tk.Text(self.TopLeft_panel, height=1, width=50, font=("Arial", 14))
        self.MemberIP_txtb.pack(anchor="w", padx=1, pady=(10,5))

        #Add Member Button
        self.Add_btn = tk.Button(self.BottomRight_panel1, text="Add", bg="green", fg="white", height=1, width=10, relief="flat",command=self.AddData)
        self.Add_btn.pack(anchor="w", padx=1, pady=1)

        #Cancel Button
        self.Cancel_btn = tk.Button(self.BottomRight_panel2, text="Cancel", bg="darkred", fg="white", height=1, width=10, relief="flat", command=self.destroy)
        self.Cancel_btn.pack(anchor="w", padx=1, pady=1)


#FUNCTIONS AND CONDITIONS SECTION ---------------------------------------------------------------------

    def AddData(self):
        member_name  = self.MemberName_txtb.get("1.0", "end").strip()
        member_ip  = self.MemberIP_txtb.get("1.0", "end").strip()

        if not member_name or not member_ip:
            print("Both fields are required!")
            return

        member_data = {
            "DeviceName": member_name,
            "DeviceIP": member_ip,
            "GroupID": ObjectId(self.group_id)
        }

        try:
            result = self.members_collection.insert_one(member_data)
            print(f"Member added successfully! {result.inserted_id}")
            self.destroy()
        except Exception as e:
            print(f"Error inserting data: {e}")
