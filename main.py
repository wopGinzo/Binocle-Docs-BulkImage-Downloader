import tkinter as tk
from tkinter import scrolledtext, font
import customtkinter as ctk
from playwright.sync_api import sync_playwright, TimeoutError
import os
import base64
from datetime import datetime
import threading
import subprocess
import shutil

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class ImageDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Binocle Viewer Bulk Image Downloader")
        self.geometry("600x750")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)  # Increased to accommodate new rows

        # URL input
        self.url_label = ctk.CTkLabel(self, text="URL:")
        self.url_label.grid(row=0, column=0, padx=20, pady=(20,0), sticky="w")
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter URL")
        self.url_entry.grid(row=1, column=0, padx=20, pady=(0,20), sticky="ew")

        # Number of images input
        self.num_images_label = ctk.CTkLabel(self, text="Number of Images:")
        self.num_images_label.grid(row=2, column=0, padx=20, pady=(20,0), sticky="w")
        self.num_images_entry = ctk.CTkEntry(self, placeholder_text="Enter number of images")
        self.num_images_entry.grid(row=3, column=0, padx=20, pady=(0,20), sticky="ew")

        # Timeout input
        self.timeout_label = ctk.CTkLabel(self, text="Timeout (seconds):")
        self.timeout_label.grid(row=4, column=0, padx=20, pady=(20,0), sticky="w")
        self.timeout_entry = ctk.CTkEntry(self, placeholder_text="Enter timeout in seconds")
        self.timeout_entry.grid(row=5, column=0, padx=20, pady=(0,20), sticky="ew")
        self.timeout_entry.insert(0, "30")  # Set default timeout to 30 seconds

        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download)
        self.download_button.grid(row=6, column=0, padx=20, pady=20)

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        self.progress_bar.set(0)

        self.open_folder_button = ctk.CTkButton(self, text="Open Download Folder", command=self.open_download_folder)
        self.open_folder_button.grid(row=8, column=0, padx=20, pady=20)

        # Styling the log area
        log_font = font.Font(family="Helvetica", size=12)
        self.log_area = scrolledtext.ScrolledText(
            self, 
            wrap=tk.WORD, 
            width=40, 
            height=10, 
            font=log_font,
            bg='#2b2b2b',  # Dark background
            fg='#ffffff',  # White text
            insertbackground='white'  # White cursor
        )
        self.log_area.grid(row=9, column=0, padx=20, pady=20, sticky="nsew")
        self.log_area.configure(state='disabled')  # Make it read-only

    def log(self, message):
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def start_download(self):
        url = self.url_entry.get().strip()
        num_images = self.num_images_entry.get().strip()
        timeout = self.timeout_entry.get().strip()

        # Check for empty fields
        if not url:
            self.log("Error: URL field is empty.")
            return
        if not num_images:
            self.log("Error: Number of images field is empty.")
            return
        if not timeout:
            self.log("Error: Timeout field is empty.")
            return

        # Validate numeric inputs
        try:
            num_images = int(num_images)
            timeout = int(timeout) * 1000  # Convert to milliseconds
        except ValueError:
            self.log("Error: Number of images and Timeout must be integers.")
            return

        self.progress_bar.set(0)
        self.log("Starting download...")

        # Disable the download button
        self.download_button.configure(state="disabled")

        thread = threading.Thread(target=self.download_images, args=(url, num_images, timeout))
        thread.start()

    def download_images(self, url, num_images, timeout):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(viewport={'width': 1920, 'height': 1080})
                page = context.new_page()
                page.set_default_timeout(timeout)

                os.makedirs("downloaded_images", exist_ok=True)
                self.log("Navigating to the provided URL..")
                page.goto(url, wait_until='networkidle')

                try:
                    title = page.locator('h1.bn-section-title').inner_text()
                except:
                    title = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                folder_name = "".join(c for c in title if c.isalnum() or c in (' ', '_')).rstrip()
                folder_path = os.path.join("downloaded_images", folder_name)
                self.log(f'Creating directory named {folder_path}..')
                os.makedirs(folder_path, exist_ok=True)

                # Check if the canvas exists
                if not page.locator('canvas.ol-unselectable').count():
                    self.log("Error: Website doesn't seem to be using Binocle Viewer.")
                    browser.close()
                    shutil.rmtree(folder_path)
                    self.log(f"Deleted directory: {folder_path}")
                    return

                for i in range(num_images):
                    try:
                        self.log(f'Fetching image {i+1} ..')
                        
                        base64_image = page.evaluate('''() => {
                            const canvas = document.querySelector('canvas.ol-unselectable');
                            return canvas.toDataURL('image/png').split(',')[1];
                        }''')

                        image_data = base64.b64decode(base64_image)
                        with open(os.path.join(folder_path, f"image_{i+1}.png"), "wb") as f:
                            f.write(image_data)

                        self.log(f"Downloaded image {i+1} successfully!")
                        self.progress_bar.set((i + 1) / num_images)

                        if i < num_images - 1:
                            next_button = page.locator('button.bn-gallery-button.bn-gallery-button-next')
                            if next_button.is_disabled():
                                self.log("No more images available. Ending the process.")
                                break
                            next_button.click()
                            page.reload(wait_until='networkidle')

                    except TimeoutError:
                        self.log(f"Timeout occurred while processing image {i+1}. Moving to next image.")
                        continue

                browser.close()
                self.log("Download completed!")
        finally:
            # Re-enable the download button
            self.download_button.configure(state="normal")

    def open_download_folder(self):
        folder_path = os.path.abspath("downloaded_images")
        if os.path.exists(folder_path):
            if os.name == 'nt':  # For Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # For macOS and Linux
                subprocess.call(('open', folder_path))
        else:
            self.log("Download folder does not exist yet.")

if __name__ == "__main__":
    app = ImageDownloaderApp()
    app.mainloop()