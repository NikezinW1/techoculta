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
    
    title_match = re.search(r"title:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if title_match: data['title'] = title_match.group(1)
        
    category_match = re.search(r"category:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if category_match: data['category'] = category_match.group(1)
        
    type_match = re.search(r"articleType:\s*['\"]?(.*?)['\"]?\n", fm_text)
    if type_match: data['articleType'] = type_match.group(1)
    
    return data

def dump_articles():
    mdx_files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))
    out = []
    
    for i, fpath in enumerate(mdx_files):
        slug = os.path.basename(fpath).replace(".mdx", "")
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        fm = parse_frontmatter(content)
        title = fm.get("title", "")
        cat = fm.get("category", "")
        atype = fm.get("articleType", "informational")
        
        out.append(f"{i+1}. {title}\n   Slug: {slug}\n   Category: {cat}\n   Type: {atype}\n")
        
    with open("scratch/articles_list.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    dump_articles()
