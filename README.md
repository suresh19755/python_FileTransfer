# python_FileTransfer
A simple Python GUI to instantly share files over local Wi-Fi. Built with Tkinter and http.server—zero external dependencies required.

# 📂 QuickFile Transfer

A simple and modern GUI application to share files across your local network (Wi-Fi) without using the internet, cables, or cloud services.

Built entirely using Python's standard library. **No `pip install` required!**

## ✨ Features

* **Zero Dependencies:** Runs on standard Python. No external libraries needed.
* **GUI Interface:** User-friendly interface built with `tkinter` (no command line knowledge needed).
* **Automatic IP Detection:** Automatically finds your local IP address for easy connection.
* **Custom Directory:** Choose any folder on your computer to share.
* **Real-time Logs:** See when the server starts, stops, or errors occur.
* **Cross-Platform:** Works on Windows, macOS, and Linux (anywhere Python runs).

## 🚀 How it Works

The application spins up Python's built-in `http.server` wrapped in a threaded GUI. It turns your selected folder into a local website that any device on the same Wi-Fi network (Phones, Tablets, Laptops) can browse to download files.

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.x installed on your machine.

### Running the App

1.  **Clone the repository** (or download `quickfile.py`):
    ```bash
    git clone [https://github.com/yourusername/QuickFile-WiFi-Transfer.git](https://github.com/yourusername/QuickFile-WiFi-Transfer.git)
    cd QuickFile-WiFi-Transfer
    ```

2.  **Run the script:**
    ```bash
    python quickfile.py
    ```

3.  **Share Files:**
    * Click **"Browse..."** to select the folder you want to share.
    * Click **"Start Server"**.
    * On your other device (e.g., your phone), open a web browser.
    * Type in the URL displayed in the app (e.g., `http://192.168.1.5:8000`).
    * Download your files!

4.  **Stop Sharing:**
    * Click **"Stop Server"** to shut down the connection immediately.

## 📸 Screenshots
*( <img width="678" height="649" alt="Screenshot 2025-11-27 001131" src="https://github.com/user-attachments/assets/a4f097f0-50e3-4942-973a-b6becaee7dc8" /> )*

## 🛡️ Security Note

This tool creates a standard HTTP server. It is designed for **home/trusted local networks**.
* **Do not** run this on public Wi-Fi (like coffee shops) unless you want strangers to see the files in the selected folder.
* Only the folder you select is exposed.

Made by [Suresh seervi]
