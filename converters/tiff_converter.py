from .base import BaseConverter
from PIL import Image
import img2pdf
import io

class TiffConverter(BaseConverter):
    """Convert TIFF files to PDF"""
    
    def __init__(self, input_file: str, output_file: str, log_widget=None):
        super().__init__(input_file, output_file)
        self.log_widget = log_widget
    
    def log(self, message: str):
        """Log message to UI if widget exists"""
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')
    
    def validate_input(self) -> bool:
        """Check if file is valid TIFF"""
        return self.input_file.suffix.lower() in ['.tiff', '.tif']
    
    def convert(self) -> bool:
        """Convert TIFF to PDF"""
        try:
            img = Image.open(self.input_file)
            image_bytes = []
            page = 0

            while True:
                try:
                    img.seek(page)
                    frame = img.copy().convert('RGB')
                    buf = io.BytesIO()
                    frame.save(buf, format='PNG')
                    image_bytes.append(buf.getvalue())
                    self.log(f"Processed page {page + 1}")
                    page += 1
                except EOFError:
                    break

            with open(self.output_file, 'wb') as f:
                f.write(img2pdf.convert(image_bytes))

            return True
        except Exception as e:
            self.log(f"Error: {e}")
            return False