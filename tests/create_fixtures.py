from PIL import Image
import os

fixtures_dir = 'tests/fixtures'
os.makedirs(fixtures_dir, exist_ok=True)

img = Image.new('RGB', (100, 100), color='red')
img.save(os.path.join(fixtures_dir, 'test.tiff'), format='TIFF')
img.save(os.path.join(fixtures_dir, 'test.png'), format='PNG')
img.save(os.path.join(fixtures_dir, 'test.jpg'), format='JPEG')

print("Test fixtures created")