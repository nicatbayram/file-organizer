import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from pathlib import Path
import threading
import time

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Set up theme settings
        self.dark_mode = tk.BooleanVar(value=False)
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(self.header_frame, text="File Organizer", font=("Arial", 24, "bold"))
        self.title_label.pack(side=tk.LEFT)
        
        self.theme_button = tk.Button(self.header_frame, text="🌙", width=3, command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT)
        
        # Create directory selection
        self.dir_frame = tk.Frame(self.main_frame)
        self.dir_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.dir_label = tk.Label(self.dir_frame, text="Directory to organize:")
        self.dir_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.dir_entry = tk.Entry(self.dir_frame)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_button = tk.Button(self.dir_frame, text="Browse", command=self.browse_directory)
        self.browse_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Create organize button
        self.organize_button = tk.Button(
            self.main_frame, 
            text="Organize Files", 
            font=("Arial", 12),
            height=2,
            command=self.start_organizing
        )
        self.organize_button.pack(fill=tk.X, pady=(0, 20))
        
        # Create progress bar
        self.progress_frame = tk.Frame(self.main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)
        
        # Create log area
        self.log_label = tk.Label(self.main_frame, text="Operation Log:", anchor="w")
        self.log_label.pack(fill=tk.X, pady=(0, 5))
        
        self.log_area = scrolledtext.ScrolledText(self.main_frame, wrap=tk.WORD, height=15)
        self.log_area.pack(fill=tk.BOTH, expand=True)
        self.log_area.config(state=tk.DISABLED)
        
        # Status bar
        self.status_bar = tk.Label(self.main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set initial theme
        self.apply_theme()
    
    def toggle_theme(self):
        self.dark_mode.set(not self.dark_mode.get())
        self.apply_theme()
    
    def apply_theme(self):
        if self.dark_mode.get():
            self.theme_button.config(text="☀️")
            
            # Dark mode colors
            bg_color = "#2E2E2E"
            fg_color = "#FFFFFF"
            entry_bg = "#3E3E3E"
            button_bg = "#404040"
            button_fg = "#FFFFFF"
            highlight_bg = "#505050"
        else:
            self.theme_button.config(text="🌙")
            
            # Light mode colors
            bg_color = "#F0F0F0"
            fg_color = "#000000"
            entry_bg = "#FFFFFF"
            button_bg = "#E0E0E0"
            button_fg = "#000000"
            highlight_bg = "#CCCCCC"
        
        # Apply theme to all widgets
        self.root.config(bg=bg_color)
        self.main_frame.config(bg=bg_color)
        self.header_frame.config(bg=bg_color)
        self.title_label.config(bg=bg_color, fg=fg_color)
        self.theme_button.config(bg=button_bg, fg=button_fg)
        self.dir_frame.config(bg=bg_color)
        self.dir_label.config(bg=bg_color, fg=fg_color)
        self.dir_entry.config(bg=entry_bg, fg=fg_color)
        self.browse_button.config(bg=button_bg, fg=button_fg)
        self.organize_button.config(bg=button_bg, fg=button_fg)
        self.progress_frame.config(bg=bg_color)
        self.log_label.config(bg=bg_color, fg=fg_color)
        self.log_area.config(bg=entry_bg, fg=fg_color)
        self.status_bar.config(bg=highlight_bg, fg=fg_color)
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)
    
    def start_organizing(self):
        directory = self.dir_entry.get()
        if not directory:
            self.update_status("Please select a directory first")
            return
        
        if not os.path.exists(directory):
            self.update_status("Directory does not exist")
            return
        
        # Clear log and start progress
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state=tk.DISABLED)
        
        self.progress_bar.start()
        self.organize_button.config(state=tk.DISABLED)
        self.update_status("Organizing files...")
        
        # Start organizing in a separate thread
        threading.Thread(target=self.organize_files, args=(directory,), daemon=True).start()
    
    def organize_files(self, directory):
        # Get all files in directory
        try:
            entries = os.scandir(directory)
            extension_folders = {}
            
            # Process each file
            for entry in entries:
                if entry.is_file():
                    file_path = Path(entry.path)
                    extension = file_path.suffix.lower()
                    
                    if extension:
                        if extension not in extension_folders:
                            folder_name = self.get_folder_name(extension)
                            folder_path = os.path.join(directory, folder_name)
                            
                            if not os.path.exists(folder_path):
                                os.makedirs(folder_path)
                            
                            extension_folders[extension] = folder_path
                        
                        destination = os.path.join(extension_folders[extension], entry.name)
                        
                        try:
                            shutil.move(entry.path, destination)
                            self.log(f"Moved: {entry.name} -> {extension_folders[extension]}")
                        except Exception as e:
                            self.log(f"Error: Could not move {entry.name} - {str(e)}")
            
            self.root.after(0, self.complete_organization, True)
        except Exception as e:
            self.log(f"Error during organization: {str(e)}")
            self.root.after(0, self.complete_organization, False)
    
    def complete_organization(self, success):
        self.progress_bar.stop()
        self.organize_button.config(state=tk.NORMAL)
        
        if success:
            self.update_status("Organization completed successfully")
        else:
            self.update_status("Organization failed")
    
    def get_folder_name(self, extension):
        extension = extension.lower()
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return "Images"
        elif extension in ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv']:
            return "Videos"
        elif extension in ['.mp3', '.wav', '.ogg', '.flac', '.aac']:
            return "Music"
        elif extension in ['.doc', '.docx', '.odt', '.rtf']:
            return "Word Documents"
        elif extension in ['.xls', '.xlsx', '.csv']:
            return "Excel Documents"
        elif extension in ['.ppt', '.pptx']:
            return "Presentations"
        elif extension in ['.pdf']:
            return "PDF Documents"
        elif extension in ['.zip', '.rar', '.7z', '.tar', '.gz']:
            return "Archives"
        elif extension in ['.exe', '.msi']:
            return "Programs"
        elif extension in ['.txt', '.md']:
            return "Text Files"
        elif extension in ['.py', '.java', '.js', '.html', '.css', '.php']:
            return "Code Files"
        else:
            return f"Other ({extension})"
    
    def log(self, message):
        self.root.after(0, self._update_log, message)
    
    def _update_log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)
    
    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()