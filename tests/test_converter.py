import unittest
import os
import tempfile
from converters import TiffConverter, PngConverter, JpgConverter

FIXTURES_DIR = 'tests/fixtures'

class TestConverters(unittest.TestCase):
    
    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.output_dir, ignore_errors=True)
    
    def test_tiff_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.tiff')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = TiffConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_png_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.png')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = PngConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_jpg_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.jpg')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = JpgConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()

import unittest
import os
import tempfile
from converters import TiffConverter, PngConverter, JpgConverter

FIXTURES_DIR = 'tests/fixtures'

class TestConverters(unittest.TestCase):
    
    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.output_dir, ignore_errors=True)
    
    def test_tiff_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.tiff')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = TiffConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_png_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.png')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = PngConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_jpg_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.jpg')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = JpgConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_batch_conversion(self):
        """Test batch conversion of multiple files"""
        input_files = [
            (os.path.join(FIXTURES_DIR, 'test.tiff'), TiffConverter),
            (os.path.join(FIXTURES_DIR, 'test.png'), PngConverter),
            (os.path.join(FIXTURES_DIR, 'test.jpg'), JpgConverter)
        ]
        
        for input_path, converter_class in input_files:
            output_path = os.path.join(self.output_dir, f'{os.path.basename(input_path)}.pdf')
            converter = converter_class(input_path, output_path, log_widget=None)
            self.assertTrue(converter.convert())
            self.assertTrue(os.path.exists(output_path))
    
    def test_auto_detect_format(self):
        """Test auto-detection of file formats"""
        files = [
            (os.path.join(FIXTURES_DIR, 'test.tiff'), TiffConverter),
            (os.path.join(FIXTURES_DIR, 'test.png'), PngConverter),
            (os.path.join(FIXTURES_DIR, 'test.jpg'), JpgConverter)
        ]
        
        for input_path, expected_converter in files:
            output_path = os.path.join(self.output_dir, f'auto_{os.path.basename(input_path)}.pdf')
            # Simulate auto-detect by checking file extension
            ext = os.path.splitext(input_path)[1].lower()
            
            if ext in ['.png']:
                converter = PngConverter(input_path, output_path, log_widget=None)
            elif ext in ['.jpg', '.jpeg']:
                converter = JpgConverter(input_path, output_path, log_widget=None)
            else:
                converter = TiffConverter(input_path, output_path, log_widget=None)
            
            self.assertTrue(converter.convert())
            self.assertTrue(os.path.exists(output_path))
    
    def test_manual_format_rejection(self):
        """Test that wrong format selection fails validation"""
        input_path = os.path.join(FIXTURES_DIR, 'test.png')
        output_path = os.path.join(self.output_dir, 'wrong_format.pdf')
        
        # Force TIFF converter on PNG file
        converter = TiffConverter(input_path, output_path, log_widget=None)
        self.assertFalse(converter.validate_input())
    
    def test_custom_output_directory(self):
        """Test conversion with custom output directory"""
        input_path = os.path.join(FIXTURES_DIR, 'test.tiff')
        custom_dir = os.path.join(self.output_dir, 'custom_output')
        os.makedirs(custom_dir, exist_ok=True)
        output_path = os.path.join(custom_dir, 'custom.pdf')
        
        converter = TiffConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
        self.assertTrue(custom_dir in output_path)
    
    def test_pdf_file_size(self):
        """Test that generated PDF has content"""
        input_path = os.path.join(FIXTURES_DIR, 'test.tiff')
        output_path = os.path.join(self.output_dir, 'size_test.pdf')
        converter = TiffConverter(input_path, output_path, log_widget=None)
        converter.convert()
        
        file_size = os.path.getsize(output_path)
        self.assertGreater(file_size, 0)

if __name__ == '__main__':
    unittest.main()