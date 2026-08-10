import os
import re
import glob

BLOG_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\content\blog"

files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))
files.sort()

# Today is 2026-08-09. All dates MUST be <= 2026-08-09 (Zero future dates!).
dates = [
    '2026-08-01',
    '2026-08-02',
    '2026-08-03',
    '2026-08-04',
    '2026-08-05',
    '2026-08-06',
    '2026-08-07',
    '2026-08-08',
    '2026-08-09',
]

num_files = len(files)
print(f"Found {num_files} MDX files to update dates.")

for idx, filepath in enumerate(files):
    date_idx = int((idx / num_files) * len(dates))
    if date_idx >= len(dates):
        date_idx = len(dates) - 1
    new_date = dates[date_idx]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = re.sub(
        r"pubDate:\s*['\"].*?['\"]",
        f"pubDate: '{new_date}'",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {os.path.basename(filepath)} -> pubDate: '{new_date}'")

print("SUCCESS: All article pubDates updated to strictly past or today dates (2026-08-01 to 2026-08-09). NO FUTURE DATES.")
