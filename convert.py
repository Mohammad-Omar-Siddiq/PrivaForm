import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import threading
import os
from converters import TiffConverter, PngConverter, JpgConverter, WebpConverter, BmpConverter, GifConverter, PdfMerger

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


class PrivaFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrivaForm")
        self.root.geometry("700x700")
        self.root.resizable(False, False)

        # Set window icon
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        self.pad = {'padx': 10, 'pady': 5}
        
        # Header
        self._build_header()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Tab 1: Converter
        self.tab_converter = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_converter, text=" Image to PDF ")
        self._build_converter_tab()

        # Tab 2: Merger
        self.tab_merger = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_merger, text=" PDF Merger ")
        self._build_merger_tab()

    def _build_header(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill='x', pady=5)
        try:
            logo_img = Image.open('icon.png')
            logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(header_frame, image=self.logo_photo)
            logo_label.pack(side='left', padx=10)
        except:
            pass
        tk.Label(header_frame, text="PrivaForm", font=("Helvetica", 16, "bold")).pack(side='left', pady=10)

    # ================= CONVERTER TAB =================
    def _build_converter_tab(self):
        self.selected_files_conv = []

        # Format dropdown
        frame_format = tk.Frame(self.tab_converter)
        frame_format.pack(fill='x', **self.pad)
        tk.Label(frame_format, text="Format:", width=12, anchor='w').pack(side='left')
        self.format_var = tk.StringVar(value='auto')
        dropdown = tk.OptionMenu(frame_format, self.format_var, 'auto', 'tiff', 'png', 'jpg', 'webp', 'bmp', 'gif')
        dropdown.pack(side='left', padx=5)
        tk.Label(frame_format, text="(Auto-detect or select manually)", fg="gray", font=("Helvetica", 9)).pack(side='left')

        # Input files
        frame_input = tk.Frame(self.tab_converter)
        frame_input.pack(fill='x', **self.pad)
        tk.Label(frame_input, text="Input File(s):", width=12, anchor='w').pack(side='left')
        tk.Button(frame_input, text="Browse", command=self.browse_input_conv).pack(side='left', padx=5)
        self.label_file_count_conv = tk.Label(frame_input, text="0 file(s) selected", fg="gray", font=("Helvetica", 9))
        self.label_file_count_conv.pack(side='left', padx=5)

        # Output name (for single file)
        frame_output_name = tk.Frame(self.tab_converter)
        frame_output_name.pack(fill='x', **self.pad)
        tk.Label(frame_output_name, text="Output Name:", width=12, anchor='w').pack(side='left')
        self.entry_output_conv = tk.Entry(frame_output_name, width=50)
        self.entry_output_conv.pack(side='left', padx=5)
        tk.Label(frame_output_name, text="(single file only)", fg="gray", font=("Helvetica", 9)).pack(side='left')

        # Output directory
        frame_output_dir = tk.Frame(self.tab_converter)
        frame_output_dir.pack(fill='x', **self.pad)
        tk.Label(frame_output_dir, text="Save To:", width=12, anchor='w').pack(side='left')
        self.entry_output_dir_conv = tk.Entry(frame_output_dir, width=45)
        self.entry_output_dir_conv.pack(side='left', padx=5)
        tk.Button(frame_output_dir, text="Browse", command=lambda: self.browse_output_dir(self.entry_output_dir_conv)).pack(side='left')

        downloads_dir = os.path.expanduser("~/Downloads")
        self.entry_output_dir_conv.insert(0, downloads_dir)

        # Convert button
        self.btn_convert = tk.Button(self.tab_converter, text="Convert to PDF", command=self.run_convert,
                         bg="#2196F3", fg="white", font=("Helvetica", 11, "bold"), padx=20, pady=5)
        self.btn_convert.pack(pady=10)

        # Progress bar
        frame_progress = tk.Frame(self.tab_converter)
        frame_progress.pack(fill='x', **self.pad)
        self.progress_bar_conv = ttk.Progressbar(frame_progress, length=400, mode='determinate', value=0)
        self.progress_bar_conv.pack(side='left', padx=5)
        self.progress_label_conv = tk.Label(frame_progress, text="0%", width=5)
        self.progress_label_conv.pack(side='left', padx=5)

        # Log area
        tk.Label(self.tab_converter, text="Progress Log:", anchor='w').pack(fill='x', padx=10)
        self.log_conv = scrolledtext.ScrolledText(self.tab_converter, height=12, state='normal', font=("Courier", 9))
        self.log_conv.pack(fill='both', expand=True, padx=10, pady=5)

    def browse_input_conv(self):
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
            self.selected_files_conv = list(paths)
            self.label_file_count_conv.config(text=f"{len(self.selected_files_conv)} file(s) selected")
            
            if len(self.selected_files_conv) == 1:
                default_name = os.path.splitext(os.path.basename(self.selected_files_conv[0]))[0]
                self.entry_output_conv.delete(0, tk.END)
                self.entry_output_conv.insert(0, default_name)

    def run_convert(self):
        input_paths = self.selected_files_conv
        output_dir = self.entry_output_dir_conv.get().strip()
        selected_format = self.format_var.get()

        if not input_paths:
            messagebox.showerror("Error", "Please select input file(s).")
            return
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return

        self.btn_convert.config(state='disabled')
        self.log_conv.delete(1.0, tk.END)
        self.progress_bar_conv['value'] = 0
        self.progress_label_conv.config(text="0%")

        def task():
            success_count = 0
            for idx, input_path in enumerate(input_paths, 1):
                try:
                    if len(input_paths) == 1:
                        custom_name = self.entry_output_conv.get().strip()
                        if custom_name:
                            output_name = custom_name if custom_name.endswith('.pdf') else custom_name + '.pdf'
                        else:
                            output_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
                    else:
                        output_name = os.path.splitext(os.path.basename(input_path))[0] + '.pdf'
                    
                    output_path = os.path.join(output_dir, output_name)
                    
                    self.log_conv.insert(tk.END, f"[{idx}/{len(input_paths)}] Converting: {os.path.basename(input_path)}...\n")
                    self.log_conv.see(tk.END)
                    
                    converter = get_converter(input_path, output_path, selected_format, self.log_conv)
                    
                    if not converter.validate_input():
                        self.log_conv.insert(tk.END, f"❌ Invalid format\n")
                        continue
                    
                    if converter.convert():
                        self.log_conv.insert(tk.END, f"✅ Saved: {output_name}\n")
                        success_count += 1
                    else:
                        self.log_conv.insert(tk.END, f"❌ Failed\n")
                    
                    self.log_conv.see(tk.END)
                    
                    progress = int((idx / len(input_paths)) * 100)
                    self.progress_bar_conv['value'] = progress
                    self.progress_label_conv.config(text=f"{progress}%")
                    self.root.update_idletasks()
                    
                except Exception as e:
                    self.log_conv.insert(tk.END, f"❌ Error: {e}\n")
                    self.log_conv.see(tk.END)
            
            self.log_conv.insert(tk.END, f"\n✅ Complete! {success_count}/{len(input_paths)} converted\n")
            self.progress_bar_conv['value'] = 100
            self.progress_label_conv.config(text="100%")
            messagebox.showinfo("Success", f"{success_count}/{len(input_paths)} file(s) converted")
            self.btn_convert.config(state='normal')

        threading.Thread(target=task, daemon=True).start()

    # ================= MERGER TAB =================
    def _build_merger_tab(self):
        # Listbox for PDF files
        frame_list = tk.Frame(self.tab_merger)
        frame_list.pack(fill='both', expand=True, **self.pad)
        
        tk.Label(frame_list, text="PDF Files to Merge (Order top to bottom):", anchor='w').pack(fill='x')
        
        # Listbox with scrollbar
        scroll = tk.Scrollbar(frame_list)
        scroll.pack(side='right', fill='y')
        self.listbox_merger = tk.Listbox(frame_list, selectmode='extended', yscrollcommand=scroll.set, height=8)
        self.listbox_merger.pack(side='left', fill='both', expand=True)
        scroll.config(command=self.listbox_merger.yview)

        # Buttons for listbox
        frame_list_btns = tk.Frame(self.tab_merger)
        frame_list_btns.pack(fill='x', padx=10)
        tk.Button(frame_list_btns, text="Add PDFs", command=self.add_pdfs).pack(side='left', padx=2)
        tk.Button(frame_list_btns, text="Remove Selected", command=self.remove_selected_pdfs).pack(side='left', padx=2)
        tk.Button(frame_list_btns, text="Move Up", command=lambda: self.move_pdf(-1)).pack(side='left', padx=2)
        tk.Button(frame_list_btns, text="Move Down", command=lambda: self.move_pdf(1)).pack(side='left', padx=2)
        tk.Button(frame_list_btns, text="Clear All", command=lambda: self.listbox_merger.delete(0, tk.END)).pack(side='left', padx=2)

        # Output Name
        frame_output_name = tk.Frame(self.tab_merger)
        frame_output_name.pack(fill='x', **self.pad)
        tk.Label(frame_output_name, text="Output Name:", width=12, anchor='w').pack(side='left')
        self.entry_output_merger = tk.Entry(frame_output_name, width=50)
        self.entry_output_merger.pack(side='left', padx=5)
        self.entry_output_merger.insert(0, "Merged_Document.pdf")

        # Output Directory
        frame_output_dir = tk.Frame(self.tab_merger)
        frame_output_dir.pack(fill='x', **self.pad)
        tk.Label(frame_output_dir, text="Save To:", width=12, anchor='w').pack(side='left')
        self.entry_output_dir_merger = tk.Entry(frame_output_dir, width=45)
        self.entry_output_dir_merger.pack(side='left', padx=5)
        tk.Button(frame_output_dir, text="Browse", command=lambda: self.browse_output_dir(self.entry_output_dir_merger)).pack(side='left')
        self.entry_output_dir_merger.insert(0, os.path.expanduser("~/Downloads"))

        # Merge Button
        self.btn_merge = tk.Button(self.tab_merger, text="Merge PDFs", command=self.run_merge,
                         bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold"), padx=20, pady=5)
        self.btn_merge.pack(pady=10)

        # Log area
        tk.Label(self.tab_merger, text="Progress Log:", anchor='w').pack(fill='x', padx=10)
        self.log_merger = scrolledtext.ScrolledText(self.tab_merger, height=8, state='normal', font=("Courier", 9))
        self.log_merger.pack(fill='both', expand=True, padx=10, pady=5)

    def add_pdfs(self):
        paths = filedialog.askopenfilenames(title="Select PDF(s)", filetypes=[("PDF Files", "*.pdf")])
        for path in paths:
            self.listbox_merger.insert(tk.END, path)

    def remove_selected_pdfs(self):
        selected = self.listbox_merger.curselection()
        for idx in reversed(selected):
            self.listbox_merger.delete(idx)

    def move_pdf(self, direction):
        selected = self.listbox_merger.curselection()
        if not selected:
            return
        
        for idx in selected:
            new_idx = idx + direction
            if 0 <= new_idx < self.listbox_merger.size():
                text = self.listbox_merger.get(idx)
                self.listbox_merger.delete(idx)
                self.listbox_merger.insert(new_idx, text)
                self.listbox_merger.selection_set(new_idx)

    def run_merge(self):
        input_paths = list(self.listbox_merger.get(0, tk.END))
        output_dir = self.entry_output_dir_merger.get().strip()
        custom_name = self.entry_output_merger.get().strip()

        if len(input_paths) < 2:
            messagebox.showerror("Error", "Please select at least 2 PDF files to merge.")
            return
        if not output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
        if not custom_name:
            messagebox.showerror("Error", "Please provide an output name.")
            return

        output_name = custom_name if custom_name.endswith('.pdf') else custom_name + '.pdf'
        output_path = os.path.join(output_dir, output_name)

        self.btn_merge.config(state='disabled')
        self.log_merger.delete(1.0, tk.END)

        def task():
            merger = PdfMerger(input_paths, output_path, self.log_merger)
            if merger.merge():
                self.log_merger.insert(tk.END, f"\n✅ Complete! Saved: {output_name}\n")
                messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved to: {output_path}")
            else:
                self.log_merger.insert(tk.END, f"\n❌ Failed to merge PDFs.\n")
                messagebox.showerror("Error", "Failed to merge PDFs. Check the log for details.")
            
            self.log_merger.see(tk.END)
            self.btn_merge.config(state='normal')

        threading.Thread(target=task, daemon=True).start()

    # ================= SHARED UTILS =================
    def browse_output_dir(self, entry_widget):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrivaFormApp(root)
    root.mainloop()