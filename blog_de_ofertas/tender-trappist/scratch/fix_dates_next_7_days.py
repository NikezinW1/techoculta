import os
import re
import glob

BLOG_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\content\blog"

files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))

# Sort files alphabetically or by cluster for a natural timeline
files.sort()

# Today is 2026-08-09. Next 7 days range from 2026-08-09 to 2026-08-16
dates = [
    '2026-08-09',
    '2026-08-10',
    '2026-08-11',
    '2026-08-12',
    '2026-08-13',
    '2026-08-14',
    '2026-08-15',
    '2026-08-16',
]

num_files = len(files)
print(f"Found {num_files} MDX files to update dates.")

for idx, filepath in enumerate(files):
    # Distribute evenly across the next 7 days
    date_idx = int((idx / num_files) * len(dates))
    if date_idx >= len(dates):
        date_idx = len(dates) - 1
    new_date = dates[date_idx]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace pubDate: '...' or pubDate: "..." with pubDate: 'YYYY-MM-DD'
    new_content = re.sub(
        r"pubDate:\s*['\"].*?['\"]",
        f"pubDate: '{new_date}'",
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Updated {os.path.basename(filepath)} -> pubDate: '{new_date}'")

print("SUCCESS: All article pubDates updated to future dates (2026-08-09 to 2026-08-16).")
