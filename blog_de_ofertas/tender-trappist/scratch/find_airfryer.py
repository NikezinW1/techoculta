import urllib.request
import json
import os
from PIL import Image, ImageEnhance, ImageDraw

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630
headers = {'User-Agent': 'NikezinIndica/1.0 (contact@nikezinindica.com)'}

# Query specific file info for "File:Air Fryer 2020.jpg" or "File:Clickon Air Fryer.jpg"
titles = ["File:Air Fryer 2020.jpg", "File:Clickon Air Fryer.jpg", "File:Airfryer.jpg"]

for title in titles:
    encoded_title = urllib.parse.quote(title)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={encoded_title}&prop=imageinfo&iiprop=url&format=json"
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_info in pages.items():
            imageinfo = page_info.get('imageinfo', [])
            if imageinfo:
                file_url = imageinfo[0].get('url')
                print("Found Air Fryer URL:", file_url)
                
                temp_path = os.path.join(OUTPUT_DIR, "temp_airfryer.jpg")
                img_req = urllib.request.Request(file_url, headers=headers)
                with urllib.request.urlopen(img_req) as resp, open(temp_path, 'wb') as f:
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
                img = enhancer.enhance(0.8)
                
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
                target_file = os.path.join(OUTPUT_DIR, "capa-melhores-air-fryers-2026.png")
                final_img.save(target_file, quality=95)
                print("SUCCESS: Saved exact Air Fryer appliance photo to", target_file)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                break
        else:
            continue
        break

    except Exception as e:
        print("Failed for title", title, e)
