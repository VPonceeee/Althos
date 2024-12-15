import tkinter as tk
import socket
import os


def get_pc_info():
    pc_name = os.getenv('COMPUTERNAME')  
    ip_address = socket.gethostbyname(socket.gethostname())
    return pc_name, ip_address

class DeviceInfo_Form(tk.Frame): 
    def __init__(self, parent):  
        super().__init__(parent) 
        
        
        pc_name, ip_address = get_pc_info()
        
        self.TopSpacer_pnl = tk.Frame(self, height=11)  
        self.TopSpacer_pnl.pack(side="top", fill="both", expand=False)

        self.Top_pnl1 = tk.Frame(self)  
        self.Top_pnl1.pack(side="top", fill="both", expand=False)

        self.Top_pnl2 = tk.Frame(self)  
        self.Top_pnl2.pack(side="top", fill="both", expand=False)

        self.DeviceName_lbl = tk.Label(self.Top_pnl1, text="", font=("Arial", 14)) 
        self.DeviceName_lbl.pack(side="left", fill="both", padx=1, pady=5)
        self.DeviceName_lbl.config(text=f"PC Name: {pc_name}")
               
        self.DeviceIP_lbl = tk.Label(self.Top_pnl2, text="", font=("Arial", 14)) 
        self.DeviceIP_lbl.pack(side="left", fill="both", padx=1, pady=5)
        self.DeviceIP_lbl.config(text=f"IP Address: {ip_address}")

  
  
       