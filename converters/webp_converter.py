# Copyright (C) 2026 Mohammad Omar Mohammad Siddiq Sheikh
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from .base import BaseConverter
from PIL import Image
import img2pdf
import io

class WebpConverter(BaseConverter):
    def __init__(self, input_file: str, output_file: str, log_widget=None):
        super().__init__(input_file, output_file)
        self.log_widget = log_widget
    
    def log(self, message: str):
        if self.log_widget:
            self.log_widget.insert('end', message + '\n')
            self.log_widget.see('end')
    
    def validate_input(self) -> bool:
        return self.input_file.suffix.lower() == '.webp'
    
    def convert(self) -> bool:
        try:
            img = Image.open(self.input_file)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            buf = io.BytesIO()
            img.save(buf, format='WEBP')
            image_bytes = [buf.getvalue()]
            self.log("Processing WEBP...")
            with open(self.output_file, 'wb') as f:
                f.write(img2pdf.convert(image_bytes))
            return True
        except Exception as e:
            self.log(f"Error: {e}")
            return False
