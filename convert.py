import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
import os
from converters import TiffConverter, PngConverter, JpgConverter

def get_converter(input_path, output_path, file_format, log_widget):
    """Return appropriate converter based on format"""
    if file_format == 'auto':
        ext = os.path.splitext(input_path)[1].lower()
        if ext in ['.png']:
            return PngConverter(input_path, output_path, log_widget)
        elif ext in ['.jpg', '.jpeg']:
            return JpgConverter(input_path, output_path, log_widget)
        else:
            return TiffConverter(input_path, output_path, log_widget)
    elif file_format == 'png':
        return PngConverter(input_path, output_path, log_widget)
    elif file_format == 'jpg':
        return JpgConverter(input_path, output_path, log_widget)
    else:
        return TiffConverter(input_path, output_path, log_widget)

def convert():
    input_path = entry_input.get()
    output_name = entry_output.get().strip()
    output_dir = entry_output_dir.get().strip()
    selected_format = format_var.get()

    if not input_path:
        messagebox.showerror("Error", "Please select an input file.")
        return
    if not output_name:
        messagebox.showerror("Error", "Please enter an output file name.")
        return
    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    if not output_name.lower().endswith('.pdf'):
        output_name += '.pdf'

    output_path = os.path.join(output_dir, output_name)

    btn_convert.config(state='disabled')
    log.delete(1.0, tk.END)

    def run():
        try:
            converter = get_converter(input_path, output_path, selected_format, log)
            
            if not converter.validate_input():
                messagebox.showerror("Error", f"Invalid file format.")
                return
            
            success = converter.convert()
            
            if success:
                log.insert(tk.END, f"\n✅ Done! Saved to:\n{output_path}\n")
                log.see(tk.END)
                messagebox.showinfo("Success", f"PDF saved to:\n{output_path}")
            else:
                messagebox.showerror("Error", "Conversion failed.")

        except Exception as e:
            log.insert(tk.END, f"\n❌ Error: {e}\n")
            messagebox.showerror("Error", str(e))

        finally:
            btn_convert.config(state='normal')

    threading.Thread(target=run, daemon=True).start()

def browse_input():
    filetypes = [
        ("All Supported", "*.tiff *.tif *.png *.jpg *.jpeg"),
        ("TIFF Files", "*.tiff *.tif"),
        ("PNG Files", "*.png"),
        ("JPG Files", "*.jpg *.jpeg"),
        ("All Files", "*.*")
    ]
    path = filedialog.askopenfilename(title="Select File", filetypes=filetypes)
    if path:
        ext = os.path.splitext(path)[1].lower()
        valid_exts = ['.tiff', '.tif', '.png', '.jpg', '.jpeg']
        
        if ext not in valid_exts:
            messagebox.showerror("Error", f"Invalid file format. Supported: TIFF, PNG, JPG")
            return
        
        entry_input.delete(0, tk.END)
        entry_input.insert(0, path)
        default_name = os.path.splitext(os.path.basename(path))[0]
        entry_output.delete(0, tk.END)
        entry_output.insert(0, default_name)

def browse_output_dir():
    path = filedialog.askdirectory(title="Select Output Directory")
    if path:
        entry_output_dir.delete(0, tk.END)
        entry_output_dir.insert(0, path)

# --- UI ---
root = tk.Tk()
root.title("PrivaForm")
root.geometry("650x550")
root.resizable(False, False)

# Set window icon
try:
    root.iconbitmap('icon.ico')
except:
    pass  # If icon not found, use default

pad = {'padx': 10, 'pady': 5}

tk.Label(root, text="PrivaForm", font=("Helvetica", 16, "bold")).pack(pady=15)

# Format dropdown
frame_format = tk.Frame(root)
frame_format.pack(fill='x', **pad)
tk.Label(frame_format, text="Format:", width=12, anchor='w').pack(side='left')
format_var = tk.StringVar(value='auto')
dropdown = tk.OptionMenu(frame_format, format_var, 'auto', 'tiff', 'png', 'jpg')
dropdown.pack(side='left', padx=5)
tk.Label(frame_format, text="(Auto-detect or select manually)", fg="gray").pack(side='left')

# Input file
frame_input = tk.Frame(root)
frame_input.pack(fill='x', **pad)
tk.Label(frame_input, text="Input File:", width=12, anchor='w').pack(side='left')
entry_input = tk.Entry(frame_input, width=45)
entry_input.pack(side='left', padx=5)
tk.Button(frame_input, text="Browse", command=browse_input).pack(side='left')

# Output name
frame_output_name = tk.Frame(root)
frame_output_name.pack(fill='x', **pad)
tk.Label(frame_output_name, text="Output Name:", width=12, anchor='w').pack(side='left')
entry_output = tk.Entry(frame_output_name, width=45)
entry_output.pack(side='left', padx=5)

# Output directory
frame_output_dir = tk.Frame(root)
frame_output_dir.pack(fill='x', **pad)
tk.Label(frame_output_dir, text="Save To:", width=12, anchor='w').pack(side='left')
entry_output_dir = tk.Entry(frame_output_dir, width=45)
entry_output_dir.pack(side='left', padx=5)
tk.Button(frame_output_dir, text="Browse", command=browse_output_dir).pack(side='left')

# Set default output to Downloads folder
downloads_dir = os.path.expanduser("~/Downloads")
entry_output_dir.insert(0, downloads_dir)

# Convert button
btn_convert = tk.Button(root, text="Convert to PDF", command=convert,
                         bg="#2196F3", fg="white", font=("Helvetica", 11, "bold"),
                         padx=20, pady=8)
btn_convert.pack(pady=10)

# Log area
tk.Label(root, text="Progress:", anchor='w').pack(fill='x', padx=10)
log = scrolledtext.ScrolledText(root, height=14, state='normal', font=("Courier", 9))
log.pack(fill='both', padx=10, pady=5)

root.mainloop()