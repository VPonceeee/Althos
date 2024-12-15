import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId
import socket
from PIL import Image, ImageTk
import io
import threading


class ViewMember(tk.Toplevel):
    def __init__(self, parent,device_name, device_ip):
        super().__init__(parent)

        #Get the Value
        self.device_name = device_name
        self.device_ip = device_ip

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
        self.ScreenHolder()
        self.keyboardMouseData()
        threading.Thread(target=self.receive_screen).start()

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
    def ScreenHolder(self):
        # Create a frame for the PictureBox content
        self.Screen_picb = tk.Frame(self.Screen_pnl, bg="lightgray", height=400, width=680,highlightbackground="black",highlightthickness=2)
        self.Screen_picb.pack(side="top", fill="x", padx=10, pady=(5,10))
        self.Screen_picb.pack_propagate(False)

        # Display message
        self.msg_label = tk.Label(self.Screen_picb, text="No Screen Available", font=("Arial", 14, "bold"), bg="lightgray",fg="black")
        self.msg_label.place(relx=0.5, rely=0.5, anchor="center") 

    def keyboardMouseData(self):

        # Display message
        msg_label = tk.Label(self.Keyboard_pnl, text="No Keyboard & Mouse Data", font=("Arial", 14, "bold"), bg="lightgray",fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center") 

    def receive_screen(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.device_ip, 5000))  
                
                while True:
                   
                    length = client_socket.recv(4)
                    if len(length) < 4:
                        break 
                    data_length = int.from_bytes(length, 'big')
                    
                    # Receive the image data
                    data = b""
                    while len(data) < data_length:
                        packet = client_socket.recv(data_length - len(data))
                        if not packet:
                            break
                        data += packet
                    
                    if data:
                       
                        image = Image.open(io.BytesIO(data))
                        image = image.resize((680, 400))  
                        photo = ImageTk.PhotoImage(image)

                        self.msg_label.config(image=photo)
                        self.msg_label.image = photo  

        except Exception as e:
            print(f"Error receiving screen: {e}")


   