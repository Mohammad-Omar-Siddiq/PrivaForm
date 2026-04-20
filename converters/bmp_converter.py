from .base import BaseConverter
from PIL import Image
import img2pdf
import io

class BmpConverter(BaseConverter):
    def __init__(self, input_file: str, output_file: str, log_widget=None):
        super().__init__(input_file, output_file)
        self.log_widget = log_widget
    
    def log(self, message: str):
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')
    
    def validate_input(self) -> bool:
        return self.input_file.suffix.lower() == '.bmp'
    
    def convert(self) -> bool:
        try:
            img = Image.open(self.input_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buf = io.BytesIO()
            img.save(buf, format='BMP')
            image_bytes = [buf.getvalue()]
            self.log("Processing BMP...")
            with open(self.output_file, 'wb') as f:
                f.write(img2pdf.convert(image_bytes))
            return True
        except Exception as e:
            self.log(f"Error: {e}")
            return False