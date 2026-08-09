import urllib.request
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630

IMAGES = {
    "capa-melhores-air-fryers-2026.png": {
        "url": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=1200&h=630&fit=crop&q=85",
        "cyan_tint": (255, 107, 0)
    }
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for filename, spec in IMAGES.items():
    print(f"Downloading & processing {filename}...")
    temp_path = os.path.join(OUTPUT_DIR, "temp_" + filename)
    req = urllib.request.Request(spec["url"], headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp, open(temp_path, 'wb') as f:
            f.write(resp.read())
            
        # Open and process image
        img = Image.open(temp_path).convert("RGB")
        img = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        
        # 1. Darken slightly to match dark tech background
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(0.65)
        
        # 2. Boost contrast
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(1.25)
        
        # 3. Add dark tech vignette (dark edges, dark slate tones)
        vignette = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 0))
        vd = ImageDraw.Draw(vignette)
        
        # Border dark vignette gradient
        for i in range(120):
            alpha = int(220 * (1 - i / 120))
            vd.rectangle([i, i, WIDTH-i, HEIGHT-i], outline=(15, 23, 42, alpha))
            
        # Cyan neon glowing border frame to match site theme
        accent = spec["cyan_tint"]
        vd.rectangle([15, 15, WIDTH-15, HEIGHT-15], outline=accent + (180,), width=3)
        vd.rectangle([18, 18, WIDTH-18, HEIGHT-18], outline=accent + (70,), width=1)
        
        img = img.convert("RGBA")
        img.paste(vignette, (0, 0), vignette)
        
        final_img = img.convert("RGB")
        final_img.save(os.path.join(OUTPUT_DIR, filename), quality=92)
        print(f"Successfully created realistic cover for {filename}!")
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")
