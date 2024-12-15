import tkinter as tk
from AddMember_Form import AddMembers
from ViewMember_Form import ViewMember
from pymongo import MongoClient
from bson import ObjectId

class ViewGroup(tk.Frame):

    def __init__(self, parent, group_name, group_id):
        super().__init__(parent)

        self.group_id = group_id

        # Frame to display member
        self.member_frame = tk.Frame(self)
        self.member_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a vertical scrollbar to the group_frame to handle overflow
        self.canvas = tk.Canvas(self.member_frame)
        self.scrollbar = tk.Scrollbar(self.member_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the buttons horizontally
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Configure the grid to allow responsiveness (keep only 1 row, expand horizontally)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        
        # Plus button inside the inner frame (placed first)
        self.plus_button = tk.Button(self.inner_frame, text="+", relief="solid", font=("Arial", 14),command=self.ShowAddMemberPage)
        self.plus_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.plus_button.config(width=20, height=6, bd=2)

        self.load_members()

    #Show Add Member page
    def ShowAddMemberPage(self):
        AddMembers(self,self.group_id).wait_window()
        self.load_members()
    
    #Show the View Member Form
    def ViewMemberPage(self,device_name, device_ip):
        ViewMember(self,device_name, device_ip).wait_window()
        #self.load_groups()

    #Display the data 
    def load_members(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        self.plus_button = tk.Button(self.inner_frame, text="+", relief="solid", font=("Arial", 14), command=self.ShowAddMemberPage)
        self.plus_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.plus_button.config(width=20, height=6, bd=2)

        # Fetch members from the database for the specific group
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            client = MongoClient(connection_string)
            db = client["ADB"]
            members_collection = db["Members"]

            members = members_collection.find({"GroupID": ObjectId(self.group_id)})

            column = 1
            for index, member in enumerate(members, start=1):
                device_name = member["DeviceName"]
                device_ip = member["DeviceIP"]

                member_button = tk.Button(self.inner_frame, text=f"{device_name}", relief="solid", font=("Arial", 14),width=20, height=6, bd=2, command=lambda name=device_name, ip=device_ip: self.ViewMemberPage(name, ip))
                member_button.grid(row=0, column=column, padx=5, pady=5, sticky="w")
                column += 1

        except Exception as e:
            print(f"Error fetching members: {e}")



