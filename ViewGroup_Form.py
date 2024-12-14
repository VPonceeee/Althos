import tkinter as tk
from AddGroup_Form import AddGroups
from pymongo import MongoClient
from bson import ObjectId

class ViewGroup(tk.Frame): 
    def __init__(self, parent, username, AccID):
        super().__init__(parent)

        # Store the username and Account ID
        self.username = username
        self.AccID = AccID

        # Frame to display groups
        self.group_frame = tk.Frame(self)
        self.group_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a vertical scrollbar to the group_frame to handle overflow
        self.canvas = tk.Canvas(self.group_frame)
        self.scrollbar = tk.Scrollbar(self.group_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the buttons horizontally
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Configure the grid to allow responsiveness (keep only 1 row, expand horizontally)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        
        # Plus button inside the inner frame (placed first)
        self.plus_button = tk.Button(self.inner_frame, text="+", relief="solid", font=("Arial", 14), command=self.ShowAddGroupPage)
        self.plus_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.plus_button.config(width=20, height=6, bd=2)

        # Load and display groups
        self.load_groups()

    def ShowAddGroupPage(self):
        AddGroups(self, self.AccID).wait_window()
        self.load_groups()

    def load_groups(self):
        # Clear the current group buttons
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Re-add the plus button inside the inner frame
        self.plus_button = tk.Button(self.inner_frame, text="+", relief="solid", font=("Arial", 14), command=self.ShowAddGroupPage)
        self.plus_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.plus_button.config(width=20, height=6, bd=2)

        # Database connection
        try:
            connection_string = "mongodb+srv://altplusf42024:RuVAh3aZgUbC0YLE@altf4cluster.9p2yp.mongodb.net/?retryWrites=true&w=majority&appName=ALTF4Cluster"
            client = MongoClient(connection_string)
            db = client["ADB"]
            groups_collection = db["Groups"]
            
            # Fetch groups created by the logged-in user
            groups = groups_collection.find({"CreatedBy": ObjectId(self.AccID)})

            # Display groups as buttons inside the inner frame horizontally
            column = 1  # Start from the second column to leave space for the plus button
            for group in groups:
                group_name = group["GroupName"]
                group_button = tk.Button(self.inner_frame, text=group_name, font=("Arial", 14), relief="solid", width=20, height=6, bd=2)
                group_button.grid(row=0, column=column, padx=5, pady=5, sticky="w")
                column += 1  # Move to the next column after each button

            # Update the scroll region to accommodate all buttons
            self.inner_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

        except Exception as e:
            print(f"Error fetching groups: {e}")
