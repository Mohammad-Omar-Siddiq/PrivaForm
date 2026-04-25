import os
import pikepdf
import io

class PdfMerger:
    """Merge multiple PDF files into one with hybrid repair logic"""
    
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
            
        opened_pdfs = []
        
        try:
            merged_pdf = pikepdf.Pdf.new()
            
            for idx, pdf_path in enumerate(self.input_files, 1):
                filename = os.path.basename(pdf_path)
                self.log(f"[{idx}/{len(self.input_files)}] Merging: {filename}...")
                
                try:
                    # Attempt 1: Standard robust open with pikepdf
                    src = pikepdf.Pdf.open(pdf_path)
                    opened_pdfs.append(src)
                    merged_pdf.pages.extend(src.pages)
                except Exception as e:
                    # Attempt 2: Hybrid Fallback
                    # If pikepdf (QPDF) fails due to structural corruption, 
                    # pypdf can sometimes still extract the pages.
                    self.log(f"  Note: {filename} has structural issues. Attempting recovery...")
                    try:
                        from pypdf import PdfReader, PdfWriter
                        
                        # Use pypdf to "re-distill" the broken PDF
                        reader = PdfReader(pdf_path, strict=False)
                        temp_writer = PdfWriter()
                        
                        page_count = 0
                        for page in reader.pages:
                            temp_writer.add_page(page)
                            page_count += 1
                        
                        if page_count == 0:
                            raise Exception("No pages could be recovered.")
                            
                        # Write the recovered pages to a memory buffer
                        temp_buf = io.BytesIO()
                        temp_writer.write(temp_buf)
                        temp_buf.seek(0)
                        
                        # Open the recovered buffer with pikepdf to continue merging
                        src = pikepdf.Pdf.open(temp_buf)
                        opened_pdfs.append(src)
                        merged_pdf.pages.extend(src.pages)
                        self.log(f"  ✅ Recovered {page_count} pages from {filename}")
                        
                    except Exception as fallback_err:
                        self.log(f"  ❌ Deep recovery failed for {filename}: {fallback_err}")
                        raise e # Raise original pikepdf error if fallback also fails

            self.log("Finalizing and saving merged PDF...")
            merged_pdf.save(self.output_file)
            merged_pdf.close()
            
            return True
        except Exception as e:
            self.log(f"Error merging PDFs: {e}")
            return False
        finally:
            for src in opened_pdfs:
                try:
                    src.close()
                except:
                    pass



