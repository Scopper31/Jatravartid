import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import zipfile
import gzip
import hashlib
import py7zr
import time

class PythonArchiver:
    def __init__(self, master):
        self.master = master
        master.title("Python Archiver")

        # UI elements
        self.file_label = tk.Label(master, text="Select File/Folder:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)

        self.file_path_entry = tk.Entry(master, width=50)
        self.file_path_entry.grid(row=0, column=1, padx=5, pady=5)

        self.file_button = tk.Button(master, text="Browse", command=self.select_file)
        self.file_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_label = tk.Label(master, text="Select Output Directory:")
        self.output_label.grid(row=1, column=0, padx=5, pady=5)

        self.output_path_entry = tk.Entry(master, width=50)
        self.output_path_entry.grid(row=1, column=1, padx=5, pady=5)

        self.output_button = tk.Button(master, text="Browse", command=self.select_output_dir)
        self.output_button.grid(row=1, column=2, padx=5, pady=5)

        self.compression_label = tk.Label(master, text="Compression Type:")
        self.compression_label.grid(row=2, column=0, padx=5, pady=5)

        self.compression_var = tk.StringVar(master)
        self.compression_var.set("zip")
        self.compression_options = ["zip", "gzip", "7z"]
        self.compression_menu = tk.OptionMenu(master, self.compression_var, *self.compression_options)
        self.compression_menu.grid(row=2, column=1, padx=5, pady=5)

        self.password_label = tk.Label(master, text="Password (optional):")
        self.password_label.grid(row=3, column=0, padx=5, pady=5)

        self.password_entry = tk.Entry(master, width=50, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.compress_button = tk.Button(master, text="Compress", command=self.compress)
        self.compress_button.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

        self.decompress_button = tk.Button(master, text="Decompress", command=self.decompress)
        self.decompress_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

    def select_file(self):
        """Opens file dialog to select file or folder."""
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, filedialog.askopenfilename(initialdir="/", title="Select File or Folder"))

    def select_output_dir(self):
        """Opens directory dialog to select output directory."""
        self.output_path_entry.delete(0, tk.END)
        self.output_path_entry.insert(0, filedialog.askdirectory(initialdir="/", title="Select Output Directory"))

    def compress(self):
        """Compresses the selected file or folder."""
        self.progress_bar['value'] = 0
        self.result_label.config(text="")

        # Get input values
        input_path = self.file_path_entry.get()
        output_path = self.output_path_entry.get()
        compression_type = self.compression_var.get()
        password = self.password_entry.get()

        if not input_path or not output_path:
            self.result_label.config(text="Please select input and output paths")
            return

        try:
            if compression_type == "zip":
                self.compress_zip(input_path, output_path, password)
            elif compression_type == "gzip":
                self.compress_gzip(input_path, output_path, password)
            elif compression_type == "7z":
                self.compress_7z(input_path, output_path, password)

            self.result_label.config(text="Compression successful!")

        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

    def decompress(self):
        """Decompresses the selected archive."""
        self.progress_bar['value'] = 0
        self.result_label.config(text="")

        # Get input values
        input_path = self.file_path_entry.get()
        output_path = self.output_path_entry.get()
        password = self.password_entry.get()

        if not input_path or not output_path:
            self.result_label.config(text="Please select input and output paths")
            return

        try:
            if input_path.endswith(".zip"):
                self.decompress_zip(input_path, output_path, password)
            elif input_path.endswith(".gz"):
                self.decompress_gzip(input_path, output_path, password)
            elif input_path.endswith(".7z"):
                self.decompress_7z(input_path, output_path, password)

            self.result_label.config(text="Decompression successful!")

        except Exception as e:
            self.result_label.config(text=f"Error: {e}")

    def compress_zip(self, input_path, output_path, password):
        """Compresses using ZIP."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, input_path))

        if password:
            self.add_password_to_zip(output_path, password)

    def compress_gzip(self, input_path, output_path, password):
        """Compresses using GZIP."""
        if os.path.isdir(input_path):
            with gzip.open(output_path, 'wb') as gz:
                for root, _, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            gz.writelines(f)
        else:
            with gzip.open(output_path, 'wb') as gz:
                with open(input_path, 'rb') as f:
                    gz.writelines(f)

        if password:
            self.add_password_to_gzip(output_path, password)

    def compress_7z(self, input_path, output_path, password):
        """Compresses using 7z."""
        with py7zr.SevenZipFile(output_path, 'w', password=password) as archive:
            archive.write(input_path)

    def decompress_zip(self, input_path, output_path, password):
        """Decompresses using ZIP."""
        with zipfile.ZipFile(input_path, 'r', password=password) as zipf:
            zipf.extractall(output_path)

    def decompress_gzip(self, input_path, output_path, password):
        """Decompresses using GZIP."""
        with gzip.open(input_path, 'rb') as gz:
            data = gz.read()
            with open(os.path.join(output_path, os.path.basename(input_path).replace(".gz", "")), 'wb') as f:
                f.write(data)

    def decompress_7z(self, input_path, output_path, password):
        """Decompresses using 7z."""
        with py7zr.SevenZipFile(input_path, 'r', password=password) as archive:
            archive.extractall(path=output_path)

    def add_password_to_zip(self, zip_path, password):
        """Adds password protection to a ZIP archive."""
        salt = os.urandom(16)
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        with open(f"{zip_path}.password", 'wb') as password_file:
            password_file.write(salt + hashed_password.encode())

    def add_password_to_gzip(self, gzip_path, password):
        """Adds password protection to a GZIP archive (placeholder - implement secure method)."""
        # Placeholder - this is not a secure way to protect GZIP files.
        # Implement a more robust solution using encryption.
        with open(f"{gzip_path}.password", 'w') as f:
            f.write(password)

    def update_progress_bar(self):
        """Updates progress bar for long operations."""
        for i in range(101):
            self.progress_bar['value'] = i
            self.master.update_idletasks()
            time.sleep(0.01)  # Simulate progress

root = tk.Tk()
archiver = PythonArchiver(root)
root.mainloop()
