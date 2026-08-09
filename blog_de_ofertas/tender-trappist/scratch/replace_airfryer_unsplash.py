import urllib.request
import os
from PIL import Image, ImageEnhance, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Unsplash Commercial License Air Fryer Photo
url = "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=1200&h=630&fit=crop&q=85"
filename = "capa-melhores-air-fryers-2026.png"
temp_path = os.path.join(OUTPUT_DIR, "temp_" + filename)

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req) as resp, open(temp_path, 'wb') as f:
        f.write(resp.read())
        
    img = Image.open(temp_path).convert("RGB")
    w, h = img.size
    target_ratio = WIDTH / HEIGHT
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))
        
    img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.75)
    
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.2)
    
    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 0))
    vd = ImageDraw.Draw(vignette)
    
    for i in range(100):
        alpha = int(210 * (1 - i / 100))
        vd.rectangle([i, i, WIDTH-i, HEIGHT-i], outline=(15, 23, 42, alpha))
        
    vd.rectangle([15, 15, WIDTH-15, HEIGHT-15], outline=(255, 107, 0, 180), width=3)
    
    img = img.convert("RGBA")
    img.paste(vignette, (0, 0), vignette)
    
    final_img = img.convert("RGB")
    target_file = os.path.join(OUTPUT_DIR, filename)
    final_img.save(target_file, quality=95)
    print("SUCCESS: Replaced Air Fryer cover with 100% Unsplash Commercial License image!")
    
    if os.path.exists(temp_path):
        os.remove(temp_path)

except Exception as e:
    print("Error:", e)
