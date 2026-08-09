import urllib.request
import json
import os
from PIL import Image, ImageEnhance, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

GAMES_IMAGES = {
    "capa-melhores-consoles-handheld-2026.png": {
        "url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=1200&h=630&fit=crop&q=85", # Retro tech / gaming handheld setup
        "accent": (0, 229, 255)
    },
    "capa-pc-portatil-vs-console-2026.png": {
        "url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=1200&h=630&fit=crop&q=85", # Futuristic gaming setup / console
        "accent": (147, 51, 234)
    },
    "capa-melhores-controles-2026.png": {
        "url": "https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=1200&h=630&fit=crop&q=85", # Wireless gaming controller
        "accent": (16, 185, 129)
    }
}

for filename, spec in GAMES_IMAGES.items():
    print(f"Downloading & processing {filename}...")
    temp_path = os.path.join(OUTPUT_DIR, "temp_" + filename)
    req = urllib.request.Request(spec["url"], headers=headers)
    
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
        
        # Darken background slightly for tech aesthetic
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.7)
        
        # Enhance contrast
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.2)
        
        # Add dark tech vignette border
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
        print(f"SUCCESS: Saved cover for {filename}")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        print(f"ERROR downloading {filename}: {e}")
