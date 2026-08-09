import urllib.request
import os
from PIL import Image, ImageEnhance, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

TV_IMAGES = {
    "capa-melhores-tvs-4k-2026.png": {
        "url": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=1200&h=630&fit=crop&q=85", # Modern 4K Smart TV
        "accent": (0, 229, 255)
    },
    "capa-oled-vs-qled-2026.png": {
        "url": "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=1200&h=630&fit=crop&q=85", # High tech screen display
        "accent": (168, 85, 247)
    },
    "capa-melhores-projetores-2026.png": {
        "url": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1200&h=630&fit=crop&q=85", # Home cinema projection
        "accent": (245, 158, 11)
    }
}

for filename, spec in TV_IMAGES.items():
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
