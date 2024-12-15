import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId


class ViewMember(tk.Toplevel):
    def __init__(self, parent,device_name, device_ip):
        super().__init__(parent)

        #Get the Value
        self.device_name = device_name
        self.device_ip = device_ip

        # Database Connection Section ---------------------------------------------------------------------


        #Form Properties Section ---------------------------------------------------------------------
        self.title(f"Monitoring - {self.device_name} ({self.device_ip})")  
        Formwidth, Formheight = 1300, 900 
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
        self.TopSpacer_panel = tk.Frame(self, height=35) 
        self.TopSpacer_panel.pack(side="top", fill="x")

        self.BottomSpacer_panel = tk.Frame(self, height=35) 
        self.BottomSpacer_panel.pack(side="bottom", fill="x")

        #Panel for Camera, Screen, Keyboard And Mouse data
        #Left Panel
        self.Left_pnl = tk.Frame(self, width=700) 
        self.Left_pnl.pack(side="left", fill="y")

        #Rigth Panel
        self.Right_pnl = tk.Frame(self, width=600) 
        self.Right_pnl.pack(side="right", fill="y")
        
        #Camera Panel
        self.Camera_pnl = tk.Frame(self.Left_pnl, height=400) 
        self.Camera_pnl.pack(side="top", fill="x")

        #Screen Panel       
        self.Screen_pnl = tk.Frame(self.Left_pnl, height=400) 
        self.Screen_pnl.pack(side="top", fill="x")

        #Keyboard Panel
        self.Keyboard_pnl = tk.Frame(self.Right_pnl, height=810,width=600,bg= "lightgray",highlightbackground="black",highlightthickness=2) 
        self.Keyboard_pnl.pack(side="top", fill="x",padx=10, pady=(10,10))
        self.Keyboard_pnl.pack_propagate(False)

        #Mouse Panel       
        #self.Mouse_pnl = tk.Frame(self.Right_pnl, height=200,width=600,bg= "red") 
        #self.Mouse_pnl.pack(side="top", fill="x",padx=10, pady=(5,10))
        #self.Mouse_pnl.pack_propagate(False)

        self.Camera_picb()
        self.Screen_picb()
        self.keyboardMouseData()


#FUNCTIONS AND CONDITIONS SECTION ---------------------------------------------------------------------

    #Camera picture box
    def Camera_picb(self):
        # Create a frame for the PictureBox content
        Camera_picb = tk.Frame(self.Camera_pnl, bg="lightgray", height=400, width=680,highlightbackground="black",highlightthickness=2)
        Camera_picb.pack(side="top", fill="x", padx=10, pady=(10,5))
        Camera_picb.pack_propagate(False)

        # Display message
        msg_label = tk.Label(Camera_picb, text="No Camera Available", font=("Arial", 14, "bold"), bg="lightgray",fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center") 

    #Screen picture box
    def Screen_picb(self):
        # Create a frame for the PictureBox content
        Screen_picb = tk.Frame(self.Screen_pnl, bg="lightgray", height=400, width=680,highlightbackground="black",highlightthickness=2)
        Screen_picb.pack(side="top", fill="x", padx=10, pady=(5,10))
        Screen_picb.pack_propagate(False)

        # Display message
        msg_label = tk.Label(Screen_picb, text="No Screen Available", font=("Arial", 14, "bold"), bg="lightgray",fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center") 

    def keyboardMouseData(self):

        # Display message
        msg_label = tk.Label(self.Keyboard_pnl, text="No Keyboard & Mouse Data", font=("Arial", 14, "bold"), bg="lightgray",fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center") 
