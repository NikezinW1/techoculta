import os
import glob
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

DIST_DIR = "e:/ofertas_telegram/blog_de_ofertas/tender-trappist/dist"

def audit_dist():
    if not os.path.exists(DIST_DIR):
        print(f"Error: {DIST_DIR} not found.")
        return

    html_files = glob.glob(os.path.join(DIST_DIR, "**/*.html"), recursive=True)
    
    total_urls = len(html_files)
    indexable_urls = []
    noindex_urls = []
    
    missing_titles = []
    missing_descriptions = []
    missing_canonical = []
    missing_h1 = []
    duplicate_h1 = []
    images_without_alt = []
    articles_no_internal_links = []
    invalid_schema = []
    og_issues = []
    
    articles = 0
    categories = 0
    institutional = 0

    for file_path in html_files:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
            
        rel_path = os.path.relpath(file_path, DIST_DIR).replace("\\", "/")
        url_path = "/" + rel_path.replace("index.html", "").strip("/")
        if not url_path.endswith("/") and url_path != "/":
            url_path += "/"
            
        # Analyze robots
        robots_meta = soup.find("meta", attrs={"name": "robots"})
        if robots_meta and "noindex" in robots_meta.get("content", "").lower():
            noindex_urls.append(url_path)
        else:
            indexable_urls.append(url_path)
            
        # Classification
        if url_path.startswith("/blog/"):
            articles += 1
        elif url_path.startswith("/categoria/"):
            categories += 1
        elif url_path in ["/sobre/", "/contato/", "/privacidade/", "/termos/", "/divulgacao-de-afiliados/"]:
            institutional += 1
            
        # Title
        title_tag = soup.find("title")
        if not title_tag or not title_tag.text.strip():
            missing_titles.append(url_path)
            
        # Description
        desc_meta = soup.find("meta", attrs={"name": "description"})
        if not desc_meta or not desc_meta.get("content", "").strip():
            missing_descriptions.append(url_path)
            
        # Canonical
        canonical_link = soup.find("link", rel="canonical")
        if not canonical_link or not canonical_link.get("href", "").strip():
            missing_canonical.append(url_path)
            
        # OG
        og_title = soup.find("meta", property="og:title")
        og_desc = soup.find("meta", property="og:description")
        og_type = soup.find("meta", property="og:type")
        if not og_title or not og_desc or not og_type:
            og_issues.append(url_path)
            
        # H1
        h1_tags = soup.find_all("h1")
        if len(h1_tags) == 0:
            missing_h1.append(url_path)
        elif len(h1_tags) > 1:
            duplicate_h1.append(url_path)
            
        # Images Alt
        images = soup.find_all("img")
        for img in images:
            alt = img.get("alt")
            if alt is None:
                images_without_alt.append(f"{url_path} -> {img.get('src')}")
                
        # Schema (JSON-LD)
        schemas = soup.find_all("script", type="application/ld+json")
        for s in schemas:
            try:
                json.loads(s.string)
            except Exception:
                invalid_schema.append(url_path)
                
        # Internal links in articles
        if url_path.startswith("/blog/"):
            main_content = soup.find("div", class_="article-content")
            if main_content:
                links = main_content.find_all("a")
                internal = [l for l in links if l.get("href", "").startswith("/") or l.get("href", "").startswith("https://nikezinindica")]
                if len(internal) == 0:
                    articles_no_internal_links.append(url_path)

    print("=== RELATÓRIO DE AUDITORIA SEO ===")
    print(f"Total de URLs em dist/: {total_urls}")
    print(f"URLs indexáveis: {len(indexable_urls)}")
    print(f"URLs noindex: {len(noindex_urls)}")
    print(f"Artigos detectados: {articles}")
    print(f"Categorias detectadas: {categories}")
    print(f"Páginas institucionais: {institutional}")
    print("\n--- PROBLEMAS ---")
    print(f"Meta titles ausentes: {len(missing_titles)}")
    print(f"Meta descriptions ausentes: {len(missing_descriptions)}")
    print(f"Canonicals ausentes: {len(missing_canonical)}")
    print(f"H1 ausentes: {len(missing_h1)}")
    if missing_h1: print("   Ex:", missing_h1[:3])
    print(f"H1 duplicados: {len(duplicate_h1)}")
    if duplicate_h1: print("   Ex:", duplicate_h1[:3])
    print(f"Imagens sem alt atributo: {len(images_without_alt)}")
    if images_without_alt: print("   Ex:", images_without_alt[:3])
    print(f"Artigos sem links internos (no conteúdo): {len(articles_no_internal_links)}")
    print(f"Schemas inválidos: {len(invalid_schema)}")
    print(f"Problemas de Open Graph: {len(og_issues)}")
    if og_issues: print("   Ex:", og_issues[:3])

if __name__ == "__main__":
    audit_dist()
