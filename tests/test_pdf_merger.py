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
from converters import PngConverter, PdfMerger

FIXTURES_DIR = 'tests/fixtures'

class TestPdfMerger(unittest.TestCase):
    
    def setUp(self):
        self.output_dir = tempfile.mkdtemp()
        
        # Create some test PDFs from PNG fixtures to use in the merger test
        self.pdf1_path = os.path.join(self.output_dir, 'test1.pdf')
        self.pdf2_path = os.path.join(self.output_dir, 'test2.pdf')
        
        png_path = os.path.join(FIXTURES_DIR, 'test.png')
        
        converter1 = PngConverter(png_path, self.pdf1_path, log_widget=None)
        converter1.convert()
        
        converter2 = PngConverter(png_path, self.pdf2_path, log_widget=None)
        converter2.convert()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.output_dir, ignore_errors=True)
    
    def test_pdf_merger_success(self):
        output_path = os.path.join(self.output_dir, 'merged.pdf')
        input_files = [self.pdf1_path, self.pdf2_path]
        
        merger = PdfMerger(input_files, output_path, log_widget=None)
        self.assertTrue(merger.merge())
        self.assertTrue(os.path.exists(output_path))
        
        # Optionally, verify the merged PDF has 2 pages
        from pypdf import PdfReader
        reader = PdfReader(output_path)
        self.assertEqual(len(reader.pages), 2)
        
    def test_pdf_merger_empty_list(self):
        output_path = os.path.join(self.output_dir, 'empty.pdf')
        input_files = []
        
        merger = PdfMerger(input_files, output_path, log_widget=None)
        self.assertFalse(merger.merge())
        self.assertFalse(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()
