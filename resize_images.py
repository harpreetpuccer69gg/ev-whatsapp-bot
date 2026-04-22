from PIL import Image
import os

W, H = 800, 400
ratio = W / H

files = [
    ('app/static/images/yuvwaa.png', False),
    ('app/static/images/fk_poster.png', True),
]

for fname, crop_left in files:
    img = Image.open(fname).convert('RGB')
    iw, ih = img.size
    print(f'{fname}: original {iw}x{ih}')
    
    if iw / ih > ratio:
        new_w = int(ih * ratio)
        left = 0 if crop_left else (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    
    img = img.resize((W, H), Image.LANCZOS)
    img.save(fname)
    print(f'{fname}: saved as {img.size}')

print('All done!')
