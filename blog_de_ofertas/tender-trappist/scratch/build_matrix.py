import os
import glob
import re
import json

BLOG_DIR = "e:/ofertas_telegram/blog_de_ofertas/tender-trappist/src/content/blog"

def parse_frontmatter(content):
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    
    fm_text = match.group(1)
    data = {}
    
    # Simple extraction
    title_match = re.search(r"title:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if title_match: data['title'] = title_match.group(1)
        
    category_match = re.search(r"category:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if category_match: data['category'] = category_match.group(1)
        
    type_match = re.search(r"articleType:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if type_match: data['articleType'] = type_match.group(1)
    
    # Tags
    tags_match = re.search(r"tags:\s*\[(.*?)\]", fm_text, re.DOTALL)
    if tags_match:
        tags_raw = tags_match.group(1)
        tags = [t.strip().strip("'\"") for t in tags_raw.split(",")]
        data['tags'] = [t for t in tags if t]
        
    return data

def build_matrix():
    mdx_files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))
    articles = []
    
    for fpath in mdx_files:
        slug = os.path.basename(fpath).replace(".mdx", "")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        fm = parse_frontmatter(content)
        
        # Count internal markdown links
        # Links like [texto](/blog/slug) or [texto](https://nikezinindica...)
        links = re.findall(r"\[.*?\]\((/blog/.*?|https://nikezinindica.*?)\)", content)
        
        articles.append({
            "slug": slug,
            "title": fm.get("title", ""),
            "category": fm.get("category", ""),
            "articleType": fm.get("articleType", "informational"),
            "tags": fm.get("tags", []),
            "internal_links": len(links),
            "content_length": len(content)
        })
        
    print(json.dumps(articles, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    build_matrix()
