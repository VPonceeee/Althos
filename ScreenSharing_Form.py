import tkinter as tk
import sys
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PIL import ImageGrab
import io

class ScreenSharing_Form(tk.Frame): 
    def __init__(self, parent):  
        super().__init__(parent)
        self.is_sharing = False
        self.thread = None
        
        # Top Spacer Panel
        self.TopSpacer_pnl = tk.Frame(self, height=10)  
        self.TopSpacer_pnl.pack(side="top", fill="both", expand=False)
        
        # Top Panel
        self.Top_pnl1 = tk.Frame(self)  
        self.Top_pnl1.pack(side="top", fill="both", expand=False)

        # Start sharing button
        self.Start_btn = tk.Button(self.Top_pnl1, text="Start Sharing", bg="lightgray", height=2, width=15, relief="flat", command=self.start_sharing)
        self.Start_btn.pack(side="left", fill="both", padx=2, pady=2)

        # Stop sharing button
        self.Stop_btn = tk.Button(self.Top_pnl1, text="Stop Sharing", bg="lightgray", height=2, width=15, relief="flat", command=self.stop_sharing)
        self.Stop_btn.pack(side="left", fill="both", padx=2, pady=2)

        # Status Label
        self.Status_lbl = tk.Label(self.Top_pnl1, text="Status", font=("Arial", 14)) 
        self.Status_lbl.pack(side="right", fill="both", padx=(1, 10), pady=5)

        # Main Panel
        self.main_panel = tk.Frame(self) 
        self.main_panel.pack(side="top", fill="both", expand=True, pady=5)

        # Status textbox 
        self.StatusMsg_txtb = tk.Text(self.main_panel, relief="sunken", bd=2, wrap="word",font=("Arial", 12))
        self.StatusMsg_txtb.pack(side="left", fill="both", expand=False)

        # Scroll Bar
        self.scrollbar = tk.Scrollbar(self.main_panel, orient="vertical", command=self.StatusMsg_txtb.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the Text widget to work with the Scrollbar
        self.StatusMsg_txtb.config(yscrollcommand=self.scrollbar.set)

        #Form Load --------------------------------------------------------------------------------
        #self.start_sharing()

    # Toggle buttons functionality
    def toggle_buttons(self):
        if self.Start_btn["state"] == "normal":
            self.Start_btn.config(state="disabled")
            self.Stop_btn.config(state="normal")
            
        else:
            self.Start_btn.config(state="normal")
            self.Stop_btn.config(state="disabled")
            

    def start_sharing(self):
        if not self.is_sharing:
            self.is_sharing = True
            self.thread = threading.Thread(target=self.run_server)
            self.thread.start()
            self.toggle_buttons()
            self.Status_lbl.config(text="Online", fg="green")
            self.StatusMsg_txtb.insert("end", "Screen sharing started...\n")

    def stop_sharing(self):
        self.is_sharing = False
        self.StatusMsg_txtb.insert("end", "Stopping screen sharing...\n")

        try:
            if self.conn:
                self.conn.close()
                self.StatusMsg_txtb.insert("end","Client connection closed.\n")

        except Exception as e:
            print(f"Error while closing client connection: {e}")

  
        try:
            if self.server_socket:
                self.server_socket.close()
                self.StatusMsg_txtb.insert("end","Server socket closed.\n")
        except Exception as e:
            print(f"Error while closing server socket: {e}")

  
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2) 
            self.StatusMsg_txtb.insert("end","Server thread stopped.\n")
        self.StatusMsg_txtb.insert("end","Screen sharing has been stopped.\n")

    def run_server(self):
        try:
            # Set up the server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", 5000))
            self.server_socket.listen(5)
            self.StatusMsg_txtb.insert("end","Server is listening for connections...\n")

            while self.is_sharing:
                try:
                    # Accept a client connection
                    self.conn, self.addr = self.server_socket.accept()
                    print(f"Connected to {self.addr}")
                    self.share_screen()
                except socket.error as e:
                    print(f"Socket error: {e}")
                finally:
                    # Clean up connection after sharing
                    if self.conn:
                        self.conn.close()
                    self.conn = None
        except Exception as e:
            print(f"Error in server: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def share_screen(self):
        try:
            while self.is_sharing and self.conn:
                # Capture the screen
                screenshot = ImageGrab.grab()
                buffer = io.BytesIO()
                screenshot.save(buffer, format="JPEG")
                data = buffer.getvalue()
                buffer.close()

                # Send the image to the client
                self.conn.sendall(len(data).to_bytes(4, 'big') + data)
                time.sleep(1)  # Adjust the interval for performance
        except (socket.error, BrokenPipeError):
            print(f"Connection lost with {self.addr}, waiting for a new connection...")
        except Exception as e:
            print(f"Error during screen sharing: {e}")
        finally:
            if self.conn:
                self.conn.close()
            self.conn = None