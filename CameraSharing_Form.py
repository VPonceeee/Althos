import tkinter as tk

class CameraSharing_Form(tk.Frame): 
    def __init__(self, parent):  
        super().__init__(parent) 
         
        self.TopSpacer_pnl = tk.Frame(self, height=10)  
        self.TopSpacer_pnl.pack(side="top", fill="both", expand=False)
        
        # Top Panel
        self.Top_pnl1 = tk.Frame(self)  
        self.Top_pnl1.pack(side="top", fill="both", expand=False)

        # Start sharing button
        self.Start_btn = tk.Button(self.Top_pnl1, text="Turn On Camera", bg="lightgray", height=2, width=15, relief="flat", command=self.toggle_buttons, state="disabled")
        self.Start_btn.pack(side="left", fill="both", padx=2, pady=2)

        # Stop sharing button
        self.Stop_btn = tk.Button(self.Top_pnl1, text="Turn Off Camera", bg="lightgray", height=2, width=15, relief="flat", command=self.toggle_buttons)
        self.Stop_btn.pack(side="left", fill="both", padx=2, pady=2)

         # Status Label
        self.Status_lbl = tk.Label(self.Top_pnl1, text="Status", font=("Arial", 14)) 
        self.Status_lbl.pack(side="right", fill="both", padx=(1, 10), pady=5)

        # Main Panel
        self.main_panel = tk.Frame(self) 
        self.main_panel.pack(side="top", fill="both", expand=True,pady=5)

        # Status textbox 
        self.StatusMsg_txtb = tk.Text(self.main_panel,relief="sunken", bd=2, wrap="none")
        self.StatusMsg_txtb.pack(side="left", fill="both", expand=True)

        # Scroll Bar
        self.scrollbar = tk.Scrollbar(self.main_panel, orient="vertical", command=self.StatusMsg_txtb.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to work with the Scrollbar
        self.StatusMsg_txtb.config(yscrollcommand=self.scrollbar.set,state="disabled")
  
    # Condition Section -------------------------------------------------------------------------------
    def toggle_buttons(self):
        if self.Start_btn["state"] == "normal":
            self.Start_btn.config(state="disabled")
            self.Stop_btn.config(state="normal")
        else:
            self.Start_btn.config(state="normal")
            self.Stop_btn.config(state="disabled")