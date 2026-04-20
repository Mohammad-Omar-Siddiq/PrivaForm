import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import threading
import os
from converters import TiffConverter, PngConverter, JpgConverter, WebpConverter, BmpConverter, GifConverter

def get_converter(input_path, output_path, file_format, log_widget):
    """Return appropriate converter based on format"""
    if file_format == 'auto':
        ext = os.path.splitext(input_path)[1].lower()
        if ext in ['.png']:
            return PngConverter(input_path, output_path, log_widget)
        elif ext in ['.jpg', '.jpeg']:
            return JpgConverter(input_path, output_path, log_widget)
        elif ext in ['.webp']:
            return WebpConverter(input_path, output_path, log_widget)
        elif ext in ['.bmp']:
            return BmpConverter(input_path, output_path, log_widget)
        elif ext in ['.gif']:
            return GifConverter(input_path, output_path, log_widget)
        else:
            return TiffConverter(input_path, output_path, log_widget)
    elif file_format == 'png':
        return PngConverter(input_path, output_path, log_widget)
    elif file_format == 'jpg':
        return JpgConverter(input_path, output_path, log_widget)
    elif file_format == 'webp':
        return WebpConverter(input_path, output_path, log_widget)
    elif file_format == 'bmp':
        return BmpConverter(input_path, output_path, log_widget)
    elif file_format == 'gif':
        return GifConverter(input_path, output_path, log_widget)
    else:
        return TiffConverter(input_path, output_path, log_widget)

def convert():
    input_paths = selected_files
    output_dir = entry_output_dir.get().strip()
    selected_format = format_var.get()

    if not input_paths:
        messagebox.showerror("Error", "Please select input file(s).")
        return
    if not output_dir:
        messagebox.showerror("Error", "Please select an output directory.")
        return

    btn_convert.config(state='disabled')
    log.delete(1.0, tk.END)
    progress_bar['value'] = 0
    progress_label.config(text="0%")

    def run():
        success_count = 0
        for idx, input_path in enumerate(input_paths, 1):
            try:
                if len(input_paths) == 1:
                    custom_name = entry_output.get().strip()
                    if custom_name:
                        output_name = custom_name if custom_name.endswith('.pdf') else custom_name + '.pdf'
                    else:
                        output_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
                else:
                    output_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
                
                output_path = os.path.join(output_dir, output_name)
                
                log.insert(tk.END, f"[{idx}/{len(input_paths)}] Converting: {os.path.basename(input_path)}...\n")
                log.see(tk.END)
                
                converter = get_converter(input_path, output_path, selected_format, log)
                
                if not converter.validate_input():
                    log.insert(tk.END, f"❌ Invalid format\n")
                    continue
                
                if converter.convert():
                    log.insert(tk.END, f"✅ Saved: {output_name}\n")
                    success_count += 1
                else:
                    log.insert(tk.END, f"❌ Failed\n")
                
                log.see(tk.END)
                
                progress = int((idx / len(input_paths)) * 100)
                progress_bar['value'] = progress
                progress_label.config(text=f"{progress}%")
                root.update_idletasks()
                
            except Exception as e:
                log.insert(tk.END, f"❌ Error: {e}\n")
                log.see(tk.END)
        
        log.insert(tk.END, f"\n✅ Complete! {success_count}/{len(input_paths)} converted\n")
        progress_bar['value'] = 100
        progress_label.config(text="100%")
        messagebox.showinfo("Success", f"{success_count}/{len(input_paths)} file(s) converted")
        btn_convert.config(state='normal')

    threading.Thread(target=run, daemon=True).start()

def browse_input():
    global selected_files
    filetypes = [
        ("All Supported", "*.tiff *.tif *.png *.jpg *.jpeg *.webp *.bmp *.gif"),
        ("TIFF Files", "*.tiff *.tif"),
        ("PNG Files", "*.png"),
        ("JPG Files", "*.jpg *.jpeg"),
        ("WEBP Files", "*.webp"),
        ("BMP Files", "*.bmp"),
        ("GIF Files", "*.gif")
    ]
    paths = filedialog.askopenfilenames(title="Select File(s)", filetypes=filetypes)
    if paths:
        selected_files = list(paths)  # All selected are already supported
        
        label_file_count.config(text=f"{len(selected_files)} file(s) selected")
        
        if len(selected_files) == 1:
            default_name = os.path.splitext(os.path.basename(selected_files[0]))[0]
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
root.geometry("700x600")
root.resizable(False, False)

# Set window icon
try:
    root.iconbitmap('icon.ico')
except:
    pass

selected_files = []

pad = {'padx': 10, 'pady': 5}

# Add logo
try:
    logo_img = Image.open('icon.png')
    logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)
except:
    pass

tk.Label(root, text="PrivaForm", font=("Helvetica", 18, "bold")).pack(pady=10)

# Format dropdown
frame_format = tk.Frame(root)
frame_format.pack(fill='x', **pad)
tk.Label(frame_format, text="Format:", width=12, anchor='w').pack(side='left')
format_var = tk.StringVar(value='auto')
dropdown = tk.OptionMenu(frame_format, format_var, 'auto', 'tiff', 'png', 'jpg', 'webp', 'bmp', 'gif')
dropdown.pack(side='left', padx=5)
tk.Label(frame_format, text="(Auto-detect or select manually)", fg="gray", font=("Helvetica", 9)).pack(side='left')

# Input files
frame_input = tk.Frame(root)
frame_input.pack(fill='x', **pad)
tk.Label(frame_input, text="Input File(s):", width=12, anchor='w').pack(side='left')
tk.Button(frame_input, text="Browse", command=browse_input).pack(side='left', padx=5)
label_file_count = tk.Label(frame_input, text="0 file(s) selected", fg="gray", font=("Helvetica", 9))
label_file_count.pack(side='left', padx=5)

# Output name (for single file)
frame_output_name = tk.Frame(root)
frame_output_name.pack(fill='x', **pad)
tk.Label(frame_output_name, text="Output Name:", width=12, anchor='w').pack(side='left')
entry_output = tk.Entry(frame_output_name, width=50)
entry_output.pack(side='left', padx=5)
tk.Label(frame_output_name, text="(single file only)", fg="gray", font=("Helvetica", 9)).pack(side='left')

# Output directory
frame_output_dir = tk.Frame(root)
frame_output_dir.pack(fill='x', **pad)
tk.Label(frame_output_dir, text="Save To:", width=12, anchor='w').pack(side='left')
entry_output_dir = tk.Entry(frame_output_dir, width=45)
entry_output_dir.pack(side='left', padx=5)
tk.Button(frame_output_dir, text="Browse", command=browse_output_dir).pack(side='left')

# Set default to Downloads
downloads_dir = os.path.expanduser("~/Downloads")
entry_output_dir.insert(0, downloads_dir)

# Convert button
btn_convert = tk.Button(root, text="Convert to PDF", command=convert,
                         bg="#2196F3", fg="white", font=("Helvetica", 11, "bold"),
                         padx=20, pady=8)
btn_convert.pack(pady=10)

# Progress bar
frame_progress = tk.Frame(root)
frame_progress.pack(fill='x', **pad)
progress_bar = ttk.Progressbar(frame_progress, length=400, mode='determinate', value=0)
progress_bar.pack(side='left', padx=5)
progress_label = tk.Label(frame_progress, text="0%", width=5)
progress_label.pack(side='left', padx=5)

# Log area
tk.Label(root, text="Progress:", anchor='w').pack(fill='x', padx=10)
log = scrolledtext.ScrolledText(root, height=12, state='normal', font=("Courier", 9))
log.pack(fill='both', padx=10, pady=5)

root.mainloop()