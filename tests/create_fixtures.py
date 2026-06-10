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


from PIL import Image
import os

fixtures_dir = 'tests/fixtures'
os.makedirs(fixtures_dir, exist_ok=True)

# Create test TIFF
img = Image.new('RGB', (100, 100), color='red')
img.save(os.path.join(fixtures_dir, 'test.tiff'), format='TIFF')

# Create test PNG
img.save(os.path.join(fixtures_dir, 'test.png'), format='PNG')

# Create test JPG
img.save(os.path.join(fixtures_dir, 'test.jpg'), format='JPEG')

# Create test WEBP
img.save(os.path.join(fixtures_dir, 'test.webp'), format='WEBP')

# Create test BMP
img.save(os.path.join(fixtures_dir, 'test.bmp'), format='BMP')

# Create static GIF
img.save(os.path.join(fixtures_dir, 'test_static.gif'), format='GIF')

# Create animated GIF
frames = [Image.new('RGB', (100, 100), color=c) for c in ['red', 'green', 'blue']]
frames[0].save(
    os.path.join(fixtures_dir, 'test_animated.gif'),
    format='GIF',
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0
)

print("Test fixtures created")
