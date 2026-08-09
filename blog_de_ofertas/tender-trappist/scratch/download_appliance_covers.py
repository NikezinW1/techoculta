import urllib.request
import os
from PIL import Image, ImageEnhance, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630

APPLIANCE_IMAGES = {
    "capa-melhores-robos-aspiradores-2026.png": {
        "urls": [
            "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=1200&h=630&fit=crop&q=85",
            "https://upload.wikimedia.org/wikipedia/commons/d/d5/Roomba_980_top.jpg"
        ],
        "accent": (0, 229, 255)
    },
    "capa-melhores-air-fryers-2026.png": {
        "urls": [
            "https://upload.wikimedia.org/wikipedia/commons/1/10/Air_fryer_closed.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/6/6f/Cosori_Air_Fryer.jpg"
        ],
        "accent": (255, 107, 0)
    }
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for filename, spec in APPLIANCE_IMAGES.items():
    success = False
    for url in spec["urls"]:
        print(f"Trying url for {filename}: {url}")
        temp_path = os.path.join(OUTPUT_DIR, "temp_" + filename)
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as resp, open(temp_path, 'wb') as f:
                f.write(resp.read())
                
            img = Image.open(temp_path).convert("RGB")
            
            # Crop center to 16:9 ratio before resizing
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
            
            # 1. Darken background slightly for tech aesthetic
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.7)
            
            # 2. Enhance contrast
            contrast = ImageEnhance.Contrast(img)
            img = contrast.enhance(1.2)
            
            # 3. Add dark tech vignette border
            vignette = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 0))
            vd = ImageDraw.Draw(vignette)
            
            for i in range(100):
                alpha = int(210 * (1 - i / 100))
                vd.rectangle([i, i, WIDTH-i, HEIGHT-i], outline=(15, 23, 42, alpha))
                
            # Accent neon border frame
            accent = spec["accent"]
            vd.rectangle([15, 15, WIDTH-15, HEIGHT-15], outline=accent + (180,), width=3)
            
            img = img.convert("RGBA")
            img.paste(vignette, (0, 0), vignette)
            
            final_img = img.convert("RGB")
            final_img.save(os.path.join(OUTPUT_DIR, filename), quality=95)
            print(f"SUCCESS: Created cover for {filename}")
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
            success = True
            break
            
        except Exception as e:
            print(f"Failed {url}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    if not success:
        print(f"ERROR: Could not download image for {filename}")
