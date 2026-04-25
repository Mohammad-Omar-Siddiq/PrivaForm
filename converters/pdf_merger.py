import os
from pypdf import PdfWriter, PdfReader

class PdfMerger:
    """Merge multiple PDF files into one"""
    
    def __init__(self, input_files: list[str], output_file: str, log_widget=None):
        self.input_files = input_files
        self.output_file = output_file
        self.log_widget = log_widget
    
    def log(self, message: str):
        """Log message to UI if widget exists"""
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')

    def merge(self) -> bool:
        """Merge PDFs. Return True if successful."""
        if not self.input_files:
            self.log("Error: No input files provided.")
            return False
            
        try:
            merger = PdfWriter()
            for idx, pdf in enumerate(self.input_files, 1):
                self.log(f"[{idx}/{len(self.input_files)}] Merging: {os.path.basename(pdf)}...")
                # Use PdfReader with strict=False to handle malformed/non-standard PDFs
                reader = PdfReader(pdf, strict=False)
                merger.append(reader)
            
            with open(self.output_file, 'wb') as f:
                merger.write(f)
            
            merger.close()
            return True
        except Exception as e:
            self.log(f"Error merging PDFs: {e}")
            return False
