import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\assets"
WIDTH, HEIGHT = 1200, 630

def create_base_canvas(start_color, end_color):
    img = Image.new("RGB", (WIDTH, HEIGHT), start_color)
    draw = ImageDraw.Draw(img)
    
    # Create diagonal gradient
    for y in range(HEIGHT):
        for x in range(WIDTH):
            factor = (x + y) / (WIDTH + HEIGHT)
            r = int(start_color[0] + factor * (end_color[0] - start_color[0]))
            g = int(start_color[1] + factor * (end_color[1] - start_color[1]))
            b = int(start_color[2] + factor * (end_color[2] - start_color[2]))
            img.putpixel((x, y), (r, g, b))
    return img

def draw_tech_grid(draw, accent_color):
    # Subtle tech grid lines
    grid_size = 40
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    for x in range(0, WIDTH, grid_size):
        d.line([(x, 0), (x, HEIGHT)], fill=(255, 255, 255, 12), width=1)
    for y in range(0, HEIGHT, grid_size):
        d.line([(0, y), (WIDTH, y)], fill=(255, 255, 255, 12), width=1)
        
    # Draw glowing accent border
    d.rectangle([20, 20, WIDTH-20, HEIGHT-20], outline=accent_color + (180,), width=3)
    d.rectangle([25, 25, WIDTH-25, HEIGHT-25], outline=accent_color + (60,), width=1)
    
    return overlay

def generate_robot_cover():
    print("Generating Robôs Aspiradores cover...")
    img = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42)) # Slate dark
    draw = ImageDraw.Draw(img)
    
    # Background radial glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([600, 100, 1100, 600], fill=(0, 229, 255, 45))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(glow, (0,0), glow)
    
    # Tech Grid
    grid = draw_tech_grid(draw, (0, 229, 255))
    img.paste(grid, (0,0), grid)
    
    # Draw Robot Vacuum Graphic
    cx, cy = 850, 350
    d = ImageDraw.Draw(img)
    # Outer body ring
    d.ellipse([cx-180, cy-180, cx+180, cy+180], fill=(30, 41, 59), outline=(0, 229, 255), width=6)
    d.ellipse([cx-160, cy-160, cx+160, cy+160], fill=(15, 23, 42), outline=(51, 65, 85), width=3)
    # LiDAR Turret
    d.ellipse([cx-45, cy-45, cx+45, cy+45], fill=(30, 41, 59), outline=(0, 229, 255), width=4)
    d.ellipse([cx-20, cy-20, cx+20, cy+20], fill=(0, 229, 255))
    # Laser Waves
    d.arc([cx-220, cy-220, cx+220, cy+220], start=200, end=340, fill=(0, 229, 255), width=3)
    d.arc([cx-260, cy-260, cx+260, cy+260], start=210, end=330, fill=(0, 229, 255), width=2)
    
    # Text overlay
    # Category Tag
    d.rectangle([80, 120, 340, 160], fill=(0, 229, 255))
    d.text((95, 130), "ELETRODOMÉSTICOS", fill=(15, 23, 42))
    
    # Title
    d.text((80, 200), "MELHORES ROBÔS\nASPIRADORES", fill=(248, 250, 252), spacing=15)
    d.text((80, 370), "Navegação a Laser, Mapeamento & Pets", fill=(0, 229, 255))
    d.text((80, 420), "GUIA DE COMPRA 2026", fill=(148, 163, 184))
    
    img.convert("RGB").save(os.path.join(OUTPUT_DIR, "capa-melhores-robos-aspiradores-2026.png"))

def generate_airfryer_cover():
    print("Generating Air Fryers cover...")
    img = Image.new("RGBA", (WIDTH, HEIGHT), (24, 15, 10)) # Dark Amber Slate
    draw = ImageDraw.Draw(img)
    
    # Background heat glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([600, 100, 1100, 600], fill=(255, 107, 0, 50))
    gd.ellipse([700, 200, 1000, 500], fill=(0, 229, 255, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(glow, (0,0), glow)
    
    # Tech Grid
    grid = draw_tech_grid(draw, (255, 107, 0))
    img.paste(grid, (0,0), grid)
    
    # Draw Air Fryer Graphic
    cx, cy = 850, 340
    d = ImageDraw.Draw(img)
    # Air Fryer Body (Curved rectangle)
    d.rounded_rectangle([cx-140, cy-170, cx+140, cy+170], radius=30, fill=(38, 24, 15), outline=(255, 107, 0), width=5)
    # Digital Display Window
    d.rounded_rectangle([cx-100, cy-140, cx+100, cy-60], radius=15, fill=(15, 23, 42), outline=(0, 229, 255), width=2)
    d.text((cx-50, cy-110), "200°C  20m", fill=(0, 229, 255))
    # Drawer Handle
    d.rounded_rectangle([cx-110, cy-20, cx+110, cy+130], radius=20, fill=(25, 18, 12), outline=(255, 107, 0), width=3)
    d.rounded_rectangle([cx-30, cy+20, cx+30, cy+90], radius=10, fill=(255, 107, 0))
    
    # Heat Vortex Rings
    for r in range(160, 220, 15):
        d.arc([cx-r, cy-r, cx+r, cy+r], start=45, end=135, fill=(255, 107, 0), width=2)
        d.arc([cx-r, cy-r, cx+r, cy+r], start=225, end=315, fill=(0, 229, 255), width=2)

    # Text overlay
    d.rectangle([80, 120, 340, 160], fill=(255, 107, 0))
    d.text((95, 130), "ELETRODOMÉSTICOS", fill=(15, 23, 42))
    
    d.text((80, 200), "MELHORES AIR FRYERS\n& FRITADEIRAS", fill=(248, 250, 252), spacing=15)
    d.text((80, 370), "Crocância, Potência & Modelos Oven/Dual Zone", fill=(255, 107, 0))
    d.text((80, 420), "GUIA DE COMPRA 2026", fill=(148, 163, 184))
    
    img.convert("RGB").save(os.path.join(OUTPUT_DIR, "capa-melhores-air-fryers-2026.png"))

def generate_lava_seca_cover():
    print("Generating Lava e Seca cover...")
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 20, 35)) # Deep Ocean Navy
    draw = ImageDraw.Draw(img)
    
    # Water Glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([600, 100, 1100, 600], fill=(0, 168, 255, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(glow, (0,0), glow)
    
    # Tech Grid
    grid = draw_tech_grid(draw, (0, 168, 255))
    img.paste(grid, (0,0), grid)
    
    # Draw Washing Machine Graphic
    cx, cy = 850, 340
    d = ImageDraw.Draw(img)
    # Machine Frame
    d.rounded_rectangle([cx-150, cy-180, cx+150, cy+180], radius=20, fill=(18, 30, 49), outline=(0, 168, 255), width=5)
    # Control Panel Top
    d.rectangle([cx-130, cy-160, cx+130, cy-110], fill=(10, 20, 35), outline=(51, 65, 85), width=2)
    d.ellipse([cx-90, cy-145, cx-70, cy-125], fill=(0, 229, 255)) # Dial
    d.text((cx-40, cy-142), "DIGITAL INVERTER", fill=(0, 168, 255))
    # Porthole Door
    d.ellipse([cx-120, cy-90, cx+120, cy+150], fill=(10, 20, 35), outline=(0, 229, 255), width=6)
    d.ellipse([cx-90, cy-60, cx+90, cy+120], fill=(20, 45, 75), outline=(0, 168, 255), width=2)
    # Water Swirl
    d.arc([cx-70, cy-40, cx+70, cy+100], start=0, end=180, fill=(0, 229, 255), width=4)
    d.arc([cx-50, cy-20, cx+50, cy+80], start=180, end=360, fill=(255, 255, 255), width=3)

    # Text overlay
    d.rectangle([80, 120, 340, 160], fill=(0, 168, 255))
    d.text((95, 130), "ELETRODOMÉSTICOS", fill=(15, 23, 42))
    
    d.text((80, 200), "MELHORES MÁQUINAS\nLAVA E SECA", fill=(248, 250, 252), spacing=15)
    d.text((80, 370), "Motores Inverter, Economia & Vapor", fill=(0, 168, 255))
    d.text((80, 420), "GUIA DE COMPRA 2026", fill=(148, 163, 184))
    
    img.convert("RGB").save(os.path.join(OUTPUT_DIR, "capa-melhores-lava-e-seca-2026.png"))

def generate_bateria_cover():
    print("Generating Celulares Bateria cover...")
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 30, 20)) # Deep Emerald Slate
    draw = ImageDraw.Draw(img)
    
    # Battery Green Glow
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([600, 100, 1100, 600], fill=(16, 185, 129, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img.paste(glow, (0,0), glow)
    
    # Tech Grid
    grid = draw_tech_grid(draw, (16, 185, 129))
    img.paste(grid, (0,0), grid)
    
    # Draw Battery Graphic
    cx, cy = 850, 340
    d = ImageDraw.Draw(img)
    # Phone Outline
    d.rounded_rectangle([cx-120, cy-180, cx+120, cy+180], radius=25, fill=(15, 23, 42), outline=(16, 185, 129), width=5)
    # Screen Battery Icon
    d.rounded_rectangle([cx-60, cy-100, cx+60, cy+100], radius=10, fill=(20, 40, 30), outline=(16, 185, 129), width=3)
    d.rectangle([cx-20, cy-115, cx+20, cy-100], fill=(16, 185, 129)) # Battery Cap
    # Charged Bars (Green)
    d.rounded_rectangle([cx-50, cy-90, cx+50, cy+90], radius=5, fill=(16, 185, 129))
    # Lightning Bolt
    d.polygon([(cx, cy-40), (cx-20, cy+10), (cx+5, cy+10), (cx-5, cy+50), (cx+25, cy-5), (cx, cy-5)], fill=(255, 255, 255))

    # Text overlay
    d.rectangle([80, 120, 260, 160], fill=(16, 185, 129))
    d.text((95, 130), "CELULARES", fill=(15, 23, 42))
    
    d.text((80, 200), "CELULARES COM\nMELHOR BATERIA", fill=(248, 250, 252), spacing=15)
    d.text((80, 370), "Modelos de 5.000 a 6.000 mAh & Carga Rápida", fill=(16, 185, 129))
    d.text((80, 420), "GUIA DE COMPRA 2026", fill=(148, 163, 184))
    
    img.convert("RGB").save(os.path.join(OUTPUT_DIR, "capa-celulares-com-melhor-bateria-2026.png"))

if __name__ == "__main__":
    generate_robot_cover()
    generate_airfryer_cover()
    generate_lava_seca_cover()
    generate_bateria_cover()
    print("ALL 4 UNIQUE COVER IMAGES GENERATED SUCCESSFULLY!")
