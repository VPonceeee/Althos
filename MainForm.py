import tkinter as tk 
from DeviceInfo_Form import DeviceInfo_Form
from ScreenSharing_Form import ScreenSharing_Form
from CameraSharing_Form import CameraSharing_Form


class MainForm(tk.Tk):
    def __init__(self): 
        super().__init__()

        # Form Section
        self.title("User App")  
        Formwidth, Formheight = 800, 600 
        self.geometry(f"{Formwidth}x{Formheight}") 
        self.resizable(False, False)  
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight() 
        x = (screen_width - Formwidth) // 2 
        y = (screen_height - Formheight) // 2  
        self.geometry(f"{Formwidth}x{Formheight}+{x}+{y}") 



        # Panel Section ---------------------------------------------------------------------
        self.left_pnl = tk.Frame(self, bg="lightgray", width=240, height=Formheight)  
        self.left_pnl.pack(side="left", fill="y", expand=False)

        self.main_panel = tk.Frame(self) 
        self.main_panel.pack(side="left", fill="both", expand=True,padx=5)

        # Button section ---------------------------------------------------------------------
        self.spacer1_pnl = tk.Frame(self.left_pnl, bg="lightgray", width=30, height=2)  
        self.spacer1_pnl.pack(side="top", fill="x", padx=10, pady=5)

        # Device Info Button
        self.deviceInfo_btn = tk.Button(self.left_pnl, text="Device Info", bg="white", height=2, width=30, relief="flat", command=self.Show_DeviceInfo)
        self.deviceInfo_btn.pack(side="top", fill="x", padx=10, pady=2)

        # Camera Service Button
        self.cam_btn = tk.Button(self.left_pnl, text="Camera Service", bg="white", height=2, width=30, relief="flat", command=self.Show_CameraSharing)
        self.cam_btn.pack(side="top", fill="x", padx=10, pady=2)

        # Screen Service Button
        self.screen_btn = tk.Button(self.left_pnl, text="Screen Service", bg="white", height=2, width=30, relief="flat", command=self.Show_ScreenSharing)
        self.screen_btn.pack(side="top", fill="x", padx=10, pady=2)

        # Stop All Service Button
        self.stop_btn = tk.Button(self.left_pnl, text="Stop All Service", bg="white", height=2, width=30, relief="flat")
        self.stop_btn.pack(side="top", fill="x", padx=10, pady=2)

        #Form Load ---------------------------------------------------------------------
        self.Show_ScreenSharing() 
        self.Show_DeviceInfo()



    def Show_DeviceInfo(self): 
        for widget in self.main_panel.winfo_children():  
            widget.destroy()  

        DeviceInfo = DeviceInfo_Form(self.main_panel) 
        DeviceInfo.pack(fill=tk.BOTH, expand=True)    

    def Show_ScreenSharing(self): 
        for widget in self.main_panel.winfo_children():  
            widget.destroy()  

        ScreenSharing = ScreenSharing_Form(self.main_panel) 
        ScreenSharing.pack(fill=tk.BOTH, expand=True)
        ScreenSharing.start_sharing()
        
    def Show_CameraSharing(self): 
        for widget in self.main_panel.winfo_children():  
            widget.destroy()  

        CameraSharing = CameraSharing_Form(self.main_panel) 
        CameraSharing.pack(fill=tk.BOTH, expand=True)  


# Start the Tkinter event loop
if __name__ == "__main__":  
    app = MainForm()  
    app.mainloop()  
