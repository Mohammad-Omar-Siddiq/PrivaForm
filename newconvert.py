import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading
from PIL import Image
import img2pdf
import io
import os

def convert():
    tiff_path = entry_input.get()
    output_name = entry_output.get().strip()

    if not tiff_path:
        messagebox.showerror("Error", "Please select a TIFF file.")
        return
    if not output_name:
        messagebox.showerror("Error", "Please enter an output file name.")
        return

    # Add .pdf extension if not present
    if not output_name.lower().endswith('.pdf'):
        output_name += '.pdf'

    output_path = os.path.join(os.path.dirname(tiff_path), output_name)

    btn_convert.config(state='disabled')
    log.delete(1.0, tk.END)

    def run():
        try:
            img = Image.open(tiff_path)
            image_bytes = []
            page = 0

            while True:
                try:
                    img.seek(page)
                    frame = img.copy().convert('RGB')
                    buf = io.BytesIO()
                    frame.save(buf, format='PNG')
                    image_bytes.append(buf.getvalue())
                    log.insert(tk.END, f"Processed page {page + 1}\n")
                    log.see(tk.END)
                    page += 1
                except EOFError:
                    break

            with open(output_path, 'wb') as f:
                f.write(img2pdf.convert(image_bytes))

            log.insert(tk.END, f"\n✅ Done! Saved to:\n{output_path}\n")
            log.see(tk.END)
            messagebox.showinfo("Success", f"PDF saved to:\n{output_path}")

        except Exception as e:
            log.insert(tk.END, f"\n❌ Error: {e}\n")
            messagebox.showerror("Error", str(e))

        finally:
            btn_convert.config(state='normal')

    threading.Thread(target=run, daemon=True).start()

def browse():
    path = filedialog.askopenfilename(
        title="Select TIFF File",
        filetypes=[("TIFF Files", "*.tiff *.tif"), ("All Files", "*.*")]
    )
    if path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, path)
        # Auto-fill output name from input filename
        default_name = os.path.splitext(os.path.basename(path))[0]
        entry_output.delete(0, tk.END)
        entry_output.insert(0, default_name)

# --- UI ---
root = tk.Tk()
root.title("PrivaForm")
root.geometry("600x450")
root.resizable(False, False)

pad = {'padx': 10, 'pady': 5}

tk.Label(root, text="PrivaForm", font=("Helvetica", 16, "bold")).pack(pady=15)

# Input file
frame_input = tk.Frame(root)
frame_input.pack(fill='x', **pad)
tk.Label(frame_input, text="Input TIFF:", width=12, anchor='w').pack(side='left')
entry_input = tk.Entry(frame_input, width=50)
entry_input.pack(side='left', padx=5)
tk.Button(frame_input, text="Browse", command=browse).pack(side='left')

# Output name
frame_output = tk.Frame(root)
frame_output.pack(fill='x', **pad)
tk.Label(frame_output, text="Output Name:", width=12, anchor='w').pack(side='left')
entry_output = tk.Entry(frame_output, width=50)
entry_output.pack(side='left', padx=5)

# Convert button
btn_convert = tk.Button(root, text="Convert to PDF", command=convert,
                         bg="#2196F3", fg="white", font=("Helvetica", 11, "bold"),
                         padx=20, pady=8)
btn_convert.pack(pady=10)

# Log area
tk.Label(root, text="Progress:", anchor='w').pack(fill='x', padx=10)
log = scrolledtext.ScrolledText(root, height=12, state='normal', font=("Courier", 9))
log.pack(fill='both', padx=10, pady=5)

root.mainloop()