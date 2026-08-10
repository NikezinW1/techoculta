import os
import glob
import re

BLOG_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\content\blog"

files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))

print(f"Total articles found: {len(files)}")

report = []

for filepath in files:
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check 1: Frontmatter title, description, pubDate
    if not re.search(r"^title:\s*['\"].+['\"]", content, re.MULTILINE):
        issues.append("Missing title in frontmatter")
    if not re.search(r"^description:\s*['\"].+['\"]", content, re.MULTILINE):
        issues.append("Missing description in frontmatter")
    
    # Check 2: Heading hierarchy check
    headings = re.findall(r"^(#{1,6})\s+(.+)", content, re.MULTILINE)
    levels = [len(h[0]) for h in headings]
    
    # Check if there is H1 in MDX body (since BlogPost layout supplies H1)
    if 1 in levels:
        issues.append("Contains H1 in MDX body (Layout already provides H1)")
        
    for i in range(len(levels) - 1):
        if levels[i+1] > levels[i] + 1:
            issues.append(f"Heading level jump from H{levels[i]} to H{levels[i+1]}: '{headings[i+1][1]}'")
            
    # Check 3: Check if commercial guide (has StoreButtons)
    has_store_buttons = "<StoreButtons" in content
    
    if has_store_buttons:
        if "tech-criteria-box" not in content:
            issues.append("Missing 'tech-criteria-box' E-E-A-T callout")
        if "| ---" not in content and "|:---" not in content and "| :---" not in content:
            issues.append("Missing Markdown Comparison Table")
        if "product-pros-cons" not in content and "Pontos Fortes" not in content:
            issues.append("Missing structured Prós e Contras")
            
    report.append((filename, issues, has_store_buttons))

print("\n--- AUDIT REPORT ---")
issues_count = 0
for filename, issues, is_guide in report:
    guide_label = "[GUIDE]" if is_guide else "[INFO]"
    if issues:
        issues_count += 1
        print(f"[FAIL] {guide_label} {filename}:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print(f"[PASS] {guide_label} {filename}: PASSED ALL SEO & E-E-A-T CHECKS")

print(f"\nTotal articles audited: {len(files)} | Articles with issues: {issues_count}")
