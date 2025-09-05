import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import platform

# Fix blurry display on Windows high-DPI screens
if platform.system() == "Windows":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)  # Enable DPI awareness
    except Exception:
        pass  # If ctypes fails, continue without DPI fix

def combine_files(input_dirs, output_file, extensions=None, exclude_dirs=None):
    """
    Combines all files in the input directories into a single output file.
    Each file's path is included as a comment before its content.
    
    Args:
        input_dirs (list): List of directories containing the files to combine.
        output_file (str): Path to the output file.
        extensions (list): List of file extensions to include (e.g., ['.py', '.js']). If None, all files are included.
        exclude_dirs (list): List of directory names to exclude (e.g., ['node_modules', 'dist']).
    """
    if not input_dirs:
        messagebox.showerror("Error", "No directories selected.")
        return False

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for input_dir in input_dirs:
                if not os.path.isdir(input_dir):
                    messagebox.showwarning("Warning", f"Skipping invalid directory: {input_dir}")
                    continue

                for root, dirs, files in os.walk(input_dir):
                    # Exclude specified directories
                    dirs[:] = [d for d in dirs if d not in (exclude_dirs or [])]
                    
                    for filename in files:
                        # Check if file has a valid extension (if extensions are specified)
                        if extensions and not any(filename.endswith(ext) for ext in extensions):
                            continue

                        file_path = os.path.join(root, filename)
                        outfile.write(f"\n\n{'='*80}\n")
                        outfile.write(f"FILE: {file_path}\n")
                        outfile.write(f"{'='*80}\n\n")
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()
                                outfile.write(content)
                        except Exception as e:
                            outfile.write(f"Error reading file: {str(e)}\n")
        messagebox.showinfo("Success", f"Files combined into {output_file}")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to combine files: {str(e)}")
        return False

class FileCombinerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Combiner")
        self.root.geometry("600x610")  # Larger window size
        self.root.resizable(True, True)  # Allow resizing
        self.selected_dirs = []
        
        # GUI Elements with better layout
        self.label = tk.Label(root, text="Select project directories to combine files. Optionally specify file extensions (e.g., .py,.js,.html).", wraplength=550, font=("Arial", 10))
        self.label.pack(pady=10)
        
        self.dir_listbox = tk.Listbox(root, height=10, width=70, font=("Arial", 9))
        self.dir_listbox.pack(pady=10)
        
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        self.add_dir_button = tk.Button(self.button_frame, text="Add Directory", command=self.add_directory, font=("Arial", 10))
        self.add_dir_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_dir_button = tk.Button(self.button_frame, text="Remove Selected Directory", command=self.remove_directory, font=("Arial", 10))
        self.remove_dir_button.pack(side=tk.LEFT, padx=5)
        
        self.extension_label = tk.Label(root, text="File extensions (comma-separated, e.g., .py,.js,.html):", font=("Arial", 10))
        self.extension_label.pack(pady=5)
        
        self.extension_entry = tk.Entry(root, width=60, font=("Arial", 9))
        self.extension_entry.insert(0, ".py,.js,.java,.dart,.jsx,.html")  # Default extensions
        self.extension_entry.pack(pady=5)
        
        self.exclude_label = tk.Label(root, text="Exclude directories (comma-separated, e.g., node_modules,dist):", font=("Arial", 10))
        self.exclude_label.pack(pady=5)
        
        self.exclude_entry = tk.Entry(root, width=60, font=("Arial", 9))
        self.exclude_entry.insert(0, "node_modules,dist,build")  # Default excluded directories
        self.exclude_entry.pack(pady=5)
        
        self.combine_button = tk.Button(root, text="Combine Files", command=self.combine_files, font=("Arial", 10))
        self.combine_button.pack(pady=20)
        
        self.exit_button = tk.Button(root, text="Exit", command=sys.exit, font=("Arial", 10))
        self.exit_button.pack(pady=10)
    
    def add_directory(self):
        """Opens a dialog to select a directory and adds it to the list."""
        directory = filedialog.askdirectory(title="Select Project Directory")
        if directory and directory not in self.selected_dirs:
            self.selected_dirs.append(directory)
            self.dir_listbox.insert(tk.END, directory)
    
    def remove_directory(self):
        """Removes the selected directory from the list."""
        selection = self.dir_listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_dirs.pop(index)
            self.dir_listbox.delete(index)
    
    def combine_files(self):
        """Combines files from selected directories."""
        if not self.selected_dirs:
            messagebox.showwarning("Warning", "No directories selected.")
            return
        
        # Get extensions from entry
        extensions_input = self.extension_entry.get()
        extensions = [ext.strip() for ext in extensions_input.split(",") if ext.strip()] if extensions_input else None
        
        # Get excluded directories from entry
        exclude_input = self.exclude_entry.get()
        exclude_dirs = [dir.strip() for dir in exclude_input.split(",") if dir.strip()] if exclude_input else []
        
        # Output file in the first selected directory
        output_file = os.path.join(self.selected_dirs[0], "combined_output.txt")
        
        # Combine files
        combine_files(self.selected_dirs, output_file, extensions, exclude_dirs)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCombinerApp(root)
    root.mainloop()