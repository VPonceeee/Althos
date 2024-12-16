import tkinter as tk
import socket
import threading
import time
from PIL import ImageGrab, Image, ImageDraw
import io
import pyautogui  # To get cursor position

class ScreenSharing_Form(tk.Frame): 
    def __init__(self, parent):  
        super().__init__(parent)
        self.is_sharing = False
        self.thread = None

        self.TopSpacer_pnl = tk.Frame(self, height=10)  
        self.TopSpacer_pnl.pack(side="top", fill="both", expand=False)
        
        self.Top_pnl1 = tk.Frame(self)  
        self.Top_pnl1.pack(side="top", fill="both", expand=False)

        self.Start_btn = tk.Button(self.Top_pnl1, text="Start Sharing", bg="lightgray", height=2, width=15, relief="flat", command=self.start_sharing)
        self.Start_btn.pack(side="left", fill="both", padx=2, pady=2)

        self.Stop_btn = tk.Button(self.Top_pnl1, text="Stop Sharing", bg="lightgray", height=2, width=15, relief="flat", command=self.stop_sharing)
        self.Stop_btn.pack(side="left", fill="both", padx=2, pady=2)

        self.Status_lbl = tk.Label(self.Top_pnl1, text="Status", font=("Arial", 14)) 
        self.Status_lbl.pack(side="right", fill="both", padx=(1, 10), pady=5)

        self.main_panel = tk.Frame(self) 
        self.main_panel.pack(side="top", fill="both", expand=True, pady=5)

        self.StatusMsg_txtb = tk.Text(self.main_panel, relief="sunken", bd=2, wrap="word", font=("Arial", 12))
        self.StatusMsg_txtb.pack(side="left", fill="both", expand=False)

        self.scrollbar = tk.Scrollbar(self.main_panel, orient="vertical", command=self.StatusMsg_txtb.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.StatusMsg_txtb.config(yscrollcommand=self.scrollbar.set)

       

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

        # Close the socket connection if it exists and is open
        if hasattr(self, 'conn') and self.conn:
            try:
                self.conn.shutdown(socket.SHUT_RDWR)  # Gracefully shutdown the socket connection
                self.conn.close()  # Close the socket
            except socket.error as e:
                print(f"Error closing connection: {e}")

        # Close the server socket if it exists and is open
        if hasattr(self, 'server_socket') and self.server_socket:
            try:
                self.server_socket.close()  # Close the server socket
            except socket.error as e:
                print(f"Error closing server socket: {e}")

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)

        self.StatusMsg_txtb.insert("end", "Screen sharing has been stopped.\n")
        self.toggle_buttons()



    def run_server(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", 5000))
            self.server_socket.listen(5)
            self.StatusMsg_txtb.insert("end", "Server is listening for connections...\n")

            while self.is_sharing:
                try:
                    self.conn, self.addr = self.server_socket.accept()
                    print(f"Connected to {self.addr}")
                    self.share_screen()
                except socket.error as e:
                    print(f"Socket error: {e}")
                finally:
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
                screenshot = ImageGrab.grab()

                # Get the cursor position
                cursor_x, cursor_y = pyautogui.position()

                # Get the cursor image (a small circle)
                cursor_image = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
                draw = ImageDraw.Draw(cursor_image)
                draw.ellipse([(0, 0), (20, 20)], fill=(255, 0, 0, 255))  # Red cursor

                # Paste the cursor image onto the screenshot at the current cursor position
                screenshot.paste(cursor_image, (cursor_x - 10, cursor_y - 10), cursor_image)

                # Convert to JPEG and send over the socket
                buffer = io.BytesIO()
                screenshot.save(buffer, format="JPEG")
                data = buffer.getvalue()
                buffer.close()

                # Send the data to the client
                self.conn.sendall(len(data).to_bytes(4, 'big') + data)
                time.sleep(1)
        except (socket.error, BrokenPipeError) as e:
            print(f"Error during screen sharing: {e}")
        finally:
            if self.conn:
                self.conn.close()
            self.conn = None

