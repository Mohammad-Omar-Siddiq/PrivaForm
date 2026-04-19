from .base import BaseConverter
from PIL import Image
import img2pdf
import io

class JpgConverter(BaseConverter):
    """Convert JPG files to PDF"""
    
    def __init__(self, input_file: str, output_file: str, log_widget=None):
        super().__init__(input_file, output_file)
        self.log_widget = log_widget
    
    def log(self, message: str):
        """Log message to UI if widget exists"""
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')
    
    def validate_input(self) -> bool:
        """Check if file is valid JPG"""
        return self.input_file.suffix.lower() in ['.jpg', '.jpeg']
    
    def convert(self) -> bool:
        """Convert JPG to PDF"""
        try:
            img = Image.open(self.input_file)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            buf = io.BytesIO()
            img.save(buf, format='JPEG')
            image_bytes = [buf.getvalue()]
            
            self.log("Processing JPG...")
            
            with open(self.output_file, 'wb') as f:
                f.write(img2pdf.convert(image_bytes))
            
            return True
        except Exception as e:
            self.log(f"Error: {e}")
            return False