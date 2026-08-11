import os
import glob
import re

BLOG_DIR = "e:/ofertas_telegram/blog_de_ofertas/tender-trappist/src/content/blog"

# Manual mapping of Slug -> Keywords to ensure natural anchors
SLUG_KEYWORDS = {
    # Hardware - SSDs
    "como-escolher-ssd-nvme-7-coisas": ["como escolher um SSD", "comprar um SSD NVMe", "escolher um SSD NVMe"],
    "capacidade-ssd-500gb-1tb-2tb-2026": ["capacidade de armazenamento", "500GB ou 1TB", "1TB ou 2TB", "capacidade do SSD"],
    "pcie-3-vs-pcie-4-2026": ["PCIe 3.0", "PCIe 4.0", "diferença entre PCIe"],
    "ssd-nvme-gen-4-ou-gen-5-2026": ["Gen 4", "Gen 5", "SSD PCIe 5.0", "SSD de quinta geração"],
    "ssd-sata-vs-nvme-2026": ["SSD SATA", "diferença entre SATA e NVMe"],
    "melhores-ssd-nvme-1tb-2026": ["SSD NVMe de 1TB", "melhores SSDs NVMe", "SSD de 1TB"],
    "melhores-ssd-para-pc-gamer-2026": ["SSD para PC gamer", "SSD para jogos", "SSD focado em games"],
    "ssd-nvme-esquentando-e-normal-como-evitar-perda-desempenho": ["SSD esquentando", "temperatura do SSD", "dissipador no SSD"],
    "crise-de-ram-e-ssd-em-2026-por-que-comprar-agora-pode-te-poupar-centenas-de-reais": ["preço das memórias", "crise de chips", "aumento de preços de SSD"],
    
    # Hardware - RAM
    "quanto-de-memoria-ram-voce-precisa-em-2026": ["quanto de memória RAM", "8GB ou 16GB", "16GB ou 32GB"],
    "ddr4-vs-ddr5-qual-a-diferenca-e-vale-a-pena-mudar-2026": ["DDR4", "DDR5", "diferença entre DDR4 e DDR5"],
    "melhores-memorias-ram-2026": ["melhores memórias RAM", "memória RAM para PC", "upgrade de memória"],
    "melhores-memrias-ram-e-ssds-para-gigabyte-b450m-gaming-vale-a-pena-em-2026": ["placa-mãe B450M", "Gigabyte B450M"],
    
    # Celulares
    "melhores-celulares-custo-beneficio-2026": ["celular custo-benefício", "smartphone custo-benefício", "melhor celular barato"],
    "melhores-celulares-para-fotos-e-videos-2026": ["celular para fotos", "celular com câmera boa", "smartphone para gravar vídeos"],
    "celulares-com-melhor-bateria-2026": ["celular com bateria boa", "smartphones com maior autonomia", "bateria duradoura"],
    "xiaomi-vs-iphone-qual-o-melhor-investimento-em-2026-para-o-seu-perfil": ["Xiaomi ou iPhone", "diferença entre iOS e Android", "iPhone vs Xiaomi"],
    
    # Redes / Wi-Fi
    "wi-fi-5-vs-wi-fi-6-vs-wi-fi-7-diferencas-2026": ["Wi-Fi 6", "Wi-Fi 7", "diferença entre Wi-Fi"],
    "melhores-roteadores-wi-fi-6-e-mesh-2026": ["roteador Wi-Fi 6", "sistema Mesh", "rede Mesh"],
    "melhores-repetidores-e-extensores-wi-fi-2026": ["repetidor Wi-Fi", "extensor de sinal", "melhorar o sinal Wi-Fi"],
    
    # Acessórios
    "carregamento-rapido-power-delivery-vs-quick-charge-2026": ["Power Delivery", "Quick Charge", "carregamento rápido"],
    "melhores-carregadores-portateis-power-bank-2026": ["power bank", "carregador portátil"],
    "melhores-hubs-usb-c-e-docks-2026": ["hub USB-C", "dock station", "adaptador USB-C"],
    
    # Áudio
    "melhores-fones-bluetooth-tws-2026": ["fones TWS", "fone Bluetooth", "fones sem fio"],
    "cancelamento-de-ruido-anc-vs-pnc-como-funciona": ["cancelamento de ruído ativo", "ANC", "isolamento passivo"],
    "headset-gamer-custo-benefcio-qual-vale-a-pena-comprar-em-2026": ["headset gamer", "fone para jogar", "headset com microfone"],
    "melhores-caixas-de-som-bluetooth-2026": ["caixa de som Bluetooth", "caixinha de som", "JBL"],
    
    # TV e Imagem
    "melhores-tvs-4k-custo-beneficio-2026": ["TV 4K", "smart TV custo-benefício"],
    "oled-vs-qled-vs-mini-led-diferencas-2026": ["TV OLED", "tela QLED", "Mini LED"],
    "melhores-projetores-portateis-2026": ["projetor portátil", "cinema em casa", "mini projetor"],
    
    # Eletrodomésticos
    "melhores-air-fryers-2026": ["Air Fryer", "fritadeira elétrica"],
    "melhores-robos-aspiradores-2026": ["robô aspirador", "aspirador inteligente"],
    "melhores-lava-e-seca-2026": ["lava e seca", "máquina de lavar inteligente"],
    
    # Games
    "melhores-consoles-e-pcs-handheld-2026": ["PC portátil", "Steam Deck", "ROG Ally", "Nintendo Switch"],
    "melhores-controles-para-pc-e-console-2026": ["controle para PC", "gamepad", "DualSense", "joystick"],
    "pc-portatil-vs-console-mesa-qual-escolher-em-2026": ["console de mesa", "PC portátil ou console"]
}

def inject_links():
    mdx_files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))
    
    total_added = 0
    modified_files = 0
    
    for fpath in mdx_files:
        slug = os.path.basename(fpath).replace(".mdx", "")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Count existing links in the body
        existing_links = len(re.findall(r"\[.*?\]\(/blog/.*?\)", content))
        if existing_links >= 3:
            # Already has enough links
            continue
            
        links_added = 0
        new_content = content
        
        # Determine category to prefer links from same category
        category_match = re.search(r"category:\s*['\"]?(.*?)['\"]?\n", content)
        my_cat = category_match.group(1) if category_match else ""
        
        # We will try to add up to 3 links
        for target_slug, keywords in SLUG_KEYWORDS.items():
            if target_slug == slug:
                continue
                
            if links_added >= 4:
                break
                
            for kw in keywords:
                # Regex to match keyword not already inside a markdown link or HTML tag
                # Uses a negative lookahead/lookbehind
                # This is tricky in pure regex, so we use a simpler approach:
                # Split content into text and tags/links, replace in text.
                
                parts = re.split(r'(\[.*?\]\(.*?\)|<[^>]+>|`.*?`)', new_content, flags=re.DOTALL)
                changed = False
                
                for i, part in enumerate(parts):
                    if i % 2 == 0:  # This is plain text
                        # Case insensitive match, but preserve original case in replacement
                        pattern = re.compile(rf'\b({re.escape(kw)})\b', re.IGNORECASE)
                        if pattern.search(part):
                            parts[i] = pattern.sub(rf'[\1](/blog/{target_slug}/)', part, count=1)
                            changed = True
                            break
                            
                if changed:
                    new_content = "".join(parts)
                    links_added += 1
                    break # Move to next target slug
                    
        if links_added > 0:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_files += 1
            total_added += links_added
            print(f"Added {links_added} links to {slug}")

    print(f"\nDone! Modified {modified_files} files, added {total_added} links in total.")

if __name__ == "__main__":
    inject_links()
