import tkinter as tk
from pymongo import MongoClient
from bson import ObjectId
import socket
from PIL import Image, ImageTk
import io
import threading


class ViewMember(tk.Toplevel):
    def __init__(self, parent, device_name, device_ip):
        super().__init__(parent)

        # Get the Value
        self.device_name = device_name
        self.device_ip = device_ip

        # Form Properties Section ---------------------------------------------------------------------
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

        # Panel for Camera, Screen, Keyboard And Mouse data
        # Left Panel
        self.Left_pnl = tk.Frame(self, width=700) 
        self.Left_pnl.pack(side="left", fill="y")

        # Right Panel
        self.Right_pnl = tk.Frame(self, width=600) 
        self.Right_pnl.pack(side="right", fill="y")
        
        # Camera Panel
        self.Camera_pnl = tk.Frame(self.Left_pnl, height=400) 
        self.Camera_pnl.pack(side="top", fill="x")

        # Screen Panel       
        self.Screen_pnl = tk.Frame(self.Left_pnl, height=400) 
        self.Screen_pnl.pack(side="top", fill="x")

        # Keyboard Panel
        self.Keyboard_pnl = tk.Frame(self.Right_pnl, height=810, width=600, bg="lightgray", highlightbackground="black", highlightthickness=2) 
        self.Keyboard_pnl.pack(side="top", fill="x", padx=10, pady=(10,10))
        self.Keyboard_pnl.pack_propagate(False)

        # Initialize components
        self.Camera_picb()
        self.ScreenHolder()
        self.keyboardMouseData()

        # Start receiving screen data in a separate thread
        threading.Thread(target=self.receive_screen, daemon=True).start()

    # FUNCTIONS AND CONDITIONS SECTION ---------------------------------------------------------------------

    # Camera picture box
    def Camera_picb(self):
        # Create a frame for the PictureBox content
        Camera_picb = tk.Frame(self.Camera_pnl, bg="lightgray", height=400, width=680, highlightbackground="black", highlightthickness=2)
        Camera_picb.pack(side="top", fill="x", padx=10, pady=(10,5))
        Camera_picb.pack_propagate(False)

        # Display message
        msg_label = tk.Label(Camera_picb, text="No Camera Available", font=("Arial", 14, "bold"), bg="lightgray", fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center")

    # Screen picture box
    def ScreenHolder(self):
        # Create a frame for the PictureBox content
        self.Screen_picb = tk.Frame(self.Screen_pnl, bg="lightgray", height=400, width=680, highlightbackground="black", highlightthickness=2)
        self.Screen_picb.pack(side="top", fill="x", padx=10, pady=(5,10))
        self.Screen_picb.pack_propagate(False)

        # Display message
        self.msg_label = tk.Label(self.Screen_picb, text="No Screen Available", font=("Arial", 14, "bold"), bg="lightgray", fg="black")
        self.msg_label.place(relx=0.5, rely=0.5, anchor="center")

    def keyboardMouseData(self):
        # Display message
        msg_label = tk.Label(self.Keyboard_pnl, text="No Keyboard & Mouse Data", font=("Arial", 14, "bold"), bg="lightgray", fg="black")
        msg_label.place(relx=0.5, rely=0.5, anchor="center")

    def receive_screen(self):
        try:
            # Attempt to connect to the sharing app (server)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(5)  # Set a timeout for the connection attempt
                try:
                    client_socket.connect((self.device_ip, 5000))  # Attempt connection to server
                    print(f"Connected to {self.device_ip}")
                    self.update_screen_status("Online")  # Indicate connection successful
                    
                    while True:
                        try:
                            length = client_socket.recv(4)
                            if len(length) < 4:
                                print("Connection closed by server.")
                                break
                            data_length = int.from_bytes(length, 'big')
                            
                            data = b""
                            while len(data) < data_length:
                                packet = client_socket.recv(data_length - len(data))
                                if not packet:
                                    print("Connection lost.")
                                    break
                                data += packet
                            
                            if data:
                                image = Image.open(io.BytesIO(data))
                                image = image.resize((680, 400))  # Resize the image for display
                                photo = ImageTk.PhotoImage(image)
                                self.msg_label.config(image=photo)
                                self.msg_label.image = photo  # Store a reference to avoid garbage collection
                        except Exception as e:
                            print(f"Error receiving screen: {e}")
                            break
                except socket.timeout:
                    print(f"Connection to {self.device_ip} timed out.")
                    self.update_screen_status("Offline")  # Indicate server is offline
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.update_screen_status("Offline")  # Indicate server is offline

    def update_screen_status(self, status):
        """ Update the screen status label based on connection status """
        if status == "Online":
            self.msg_label.config(text="Receiving Screen", font=("Arial", 14, "bold"), bg="lightgreen", fg="black")
        elif status == "Offline":
            self.msg_label.config(text="No Screen Available", font=("Arial", 14, "bold"), bg="lightgray", fg="black")
