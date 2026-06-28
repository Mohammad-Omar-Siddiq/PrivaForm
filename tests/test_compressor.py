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

import unittest
import os
import tempfile
from converters import PngConverter, JpgConverter, PdfCompressor
from pypdf import PdfReader

FIXTURES_DIR = 'tests/fixtures'

class TestPdfCompressor(unittest.TestCase):

    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        self.input_png = os.path.join(FIXTURES_DIR, 'test.png')
        self.input_jpg = os.path.join(FIXTURES_DIR, 'test.jpg')

        # Create a standard uncompressed PDF to test compression on
        self.uncompressed_pdf = os.path.join(self.output_dir, 'uncompressed.pdf')
        converter = PngConverter(self.input_png, self.uncompressed_pdf, log_widget=None, image_quality=100)
        converter.convert()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_standalone_compression(self):
        compressed_pdf = os.path.join(self.output_dir, 'compressed.pdf')
        compressor = PdfCompressor(self.uncompressed_pdf, compressed_pdf, log_widget=None)
        
        self.assertTrue(compressor.compress())
        self.assertTrue(os.path.exists(compressed_pdf))
        
        # Verify page count is preserved
        reader = PdfReader(compressed_pdf)
        self.assertEqual(len(reader.pages), 1)

    def test_image_quality_slider_effect(self):
        # Convert with quality=100
        pdf_q100 = os.path.join(self.output_dir, 'q100.pdf')
        conv_q100 = JpgConverter(self.input_jpg, pdf_q100, log_widget=None, image_quality=100)
        self.assertTrue(conv_q100.convert())

        # Convert with quality=20
        pdf_q20 = os.path.join(self.output_dir, 'q20.pdf')
        conv_q20 = JpgConverter(self.input_jpg, pdf_q20, log_widget=None, image_quality=20)
        self.assertTrue(conv_q20.convert())

        # Assert files exist
        self.assertTrue(os.path.exists(pdf_q100))
        self.assertTrue(os.path.exists(pdf_q20))

        # Size of q20 PDF should be significantly smaller than q100
        size_q100 = os.path.getsize(pdf_q100)
        size_q20 = os.path.getsize(pdf_q20)
        
        self.assertLess(size_q20, size_q100)

    def test_compressor_invalid_input(self):
        compressed_pdf = os.path.join(self.output_dir, 'invalid_compressed.pdf')
        compressor = PdfCompressor('', compressed_pdf, log_widget=None)
        self.assertFalse(compressor.compress())

if __name__ == '__main__':
    unittest.main()
