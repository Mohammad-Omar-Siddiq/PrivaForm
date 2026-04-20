import unittest
import os
import tempfile
from converters import TiffConverter, PngConverter, JpgConverter, WebpConverter, BmpConverter, GifConverter

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
    
    def test_webp_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.webp')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = WebpConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_bmp_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test.bmp')
        output_path = os.path.join(self.output_dir, 'test.pdf')
        converter = BmpConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_gif_static_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test_static.gif')
        output_path = os.path.join(self.output_dir, 'test_static.pdf')
        converter = GifConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_gif_animated_conversion(self):
        input_path = os.path.join(FIXTURES_DIR, 'test_animated.gif')
        output_path = os.path.join(self.output_dir, 'test_animated.pdf')
        converter = GifConverter(input_path, output_path, log_widget=None)
        self.assertTrue(converter.validate_input())
        self.assertTrue(converter.convert())
        self.assertTrue(os.path.exists(output_path))
    
    def test_batch_conversion_all_formats(self):
        input_files = [
            os.path.join(FIXTURES_DIR, 'test.tiff'),
            os.path.join(FIXTURES_DIR, 'test.png'),
            os.path.join(FIXTURES_DIR, 'test.jpg'),
            os.path.join(FIXTURES_DIR, 'test.webp'),
            os.path.join(FIXTURES_DIR, 'test.bmp'),
            os.path.join(FIXTURES_DIR, 'test_static.gif')
        ]
        
        converters_map = {
            '.tiff': TiffConverter,
            '.tif': TiffConverter,
            '.png': PngConverter,
            '.jpg': JpgConverter,
            '.jpeg': JpgConverter,
            '.webp': WebpConverter,
            '.bmp': BmpConverter,
            '.gif': GifConverter
        }
        
        for input_path in input_files:
            ext = os.path.splitext(input_path)[1].lower()
            converter_class = converters_map[ext]
            converter = converter_class(input_path, os.path.join(self.output_dir, f'batch_{os.path.basename(input_path)}.pdf'), log_widget=None)
            self.assertTrue(converter.convert())

if __name__ == '__main__':
    unittest.main()