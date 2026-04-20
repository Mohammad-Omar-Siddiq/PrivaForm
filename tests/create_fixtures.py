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