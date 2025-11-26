import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import http.server
import socketserver
import socket
import os
import threading
import webbrowser
import sys

class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local File Transfer Server")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # State variables
        self.server_thread = None
        self.httpd = None
        self.is_running = False
        self.port = 8000
        self.selected_dir = os.getcwd()

        # GUI Styling
        bg_color = "#f0f0f0"
        self.root.configure(bg=bg_color)
        
        # --- Header ---
        header_frame = tk.Frame(root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(header_frame, text="Wi-Fi File Sharer", font=("Segoe UI", 18, "bold"), fg="white", bg="#2c3e50")
        title_label.pack(pady=10)

        # --- Main Content ---
        main_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Directory Selection
        dir_frame = tk.Frame(main_frame, bg=bg_color)
        dir_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(dir_frame, text="Shared Folder:", font=("Segoe UI", 10, "bold"), bg=bg_color).pack(anchor="w")
        
        self.path_entry = tk.Entry(dir_frame, width=40, font=("Segoe UI", 10))
        self.path_entry.insert(0, self.selected_dir)
        self.path_entry.config(state='readonly')
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(dir_frame, text="Browse...", command=self.select_directory, bg="#ecf0f1")
        browse_btn.pack(side=tk.RIGHT)

        # Info Display (IP & URL)
        info_frame = tk.LabelFrame(main_frame, text="Connection Info", font=("Segoe UI", 10, "bold"), bg=bg_color, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=15)

        self.ip_address = self.get_local_ip()
        self.url_label = tk.Label(info_frame, text=f"http://{self.ip_address}:{self.port}", font=("Consolas", 16, "bold"), fg="#2980b9", bg=bg_color)
        self.url_label.pack(pady=5)
        
        tk.Label(info_frame, text="Type the URL above into your phone/laptop browser", font=("Segoe UI", 9), fg="#7f8c8d", bg=bg_color).pack()

        # Control Buttons
        btn_frame = tk.Frame(main_frame, bg=bg_color)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Start Server", command=self.start_server, bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"), width=12, height=1, cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="Stop Server", command=self.stop_server, bg="#c0392b", fg="white", font=("Segoe UI", 11, "bold"), width=12, height=1, state=tk.DISABLED, cursor="hand2")
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        open_browser_btn = tk.Button(btn_frame, text="Open Local", command=self.open_browser, bg="#34495e", fg="white", font=("Segoe UI", 11), width=10)
        open_browser_btn.pack(side=tk.LEFT, padx=10)

        # Logs
        tk.Label(main_frame, text="Status Logs:", font=("Segoe UI", 9, "bold"), bg=bg_color).pack(anchor="w", pady=(10,0))
        self.log_area = scrolledtext.ScrolledText(main_frame, height=6, font=("Consolas", 9), state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.log("Ready to start.")

    def get_local_ip(self):
        """Robustly finds the local IP address."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def select_directory(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_dir = folder
            self.path_entry.config(state='normal')
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.selected_dir)
            self.path_entry.config(state='readonly')
            self.log(f"Selected folder: {os.path.basename(folder)}")

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f">> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_server(self):
        if self.is_running:
            return

        try:
            # Change directory to the selected one so http.server serves it
            os.chdir(self.selected_dir)
            
            handler = http.server.SimpleHTTPRequestHandler
            
            # Create server with allow_reuse_address to avoid "Port already in use"
            socketserver.TCPServer.allow_reuse_address = True
            self.httpd = socketserver.TCPServer(("", self.port), handler)
           
            self.server_thread = threading.Thread(target=self.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_running = True
            self.update_ui_state(running=True)
            self.log(f"Server started on port {self.port}")
            self.log(f"Sharing: {self.selected_dir}")
            
        except OSError as e:
            messagebox.showerror("Error", f"Port {self.port} is busy or invalid.\nError: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server.\nError: {e}")

    def serve_forever(self):
        """Target function for the thread"""
        try:
            self.httpd.serve_forever()
        except Exception as e:
            pass

    def stop_server(self):
        if self.is_running and self.httpd:
            self.log("Stopping server...")
            # Shutdown needs to run in a separate thread if called from the main thread
            # However, shutdown() blocks, so we run it in a thread to keep UI alive
            shutdown_thread = threading.Thread(target=self._shutdown_server_logic)
            shutdown_thread.start()

    def _shutdown_server_logic(self):
        """Actual shutdown logic"""
        try:
            self.httpd.shutdown()
            self.httpd.server_close()
            self.is_running = False
            self.root.after(0, lambda: self.update_ui_state(running=False))
            self.root.after(0, lambda: self.log("Server stopped."))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error stopping: {e}"))

    def update_ui_state(self, running):
        if running:
            self.start_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.stop_btn.config(state=tk.NORMAL, bg="#c0392b")
            self.url_label.config(fg="#27ae60") 
        else:
            self.start_btn.config(state=tk.NORMAL, bg="#27ae60")
            self.stop_btn.config(state=tk.DISABLED, bg="#95a5a6")
            self.url_label.config(fg="#2980b9")

    def open_browser(self):
        webbrowser.open(f"http://localhost:{self.port}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileTransferApp(root)
    root.mainloop()