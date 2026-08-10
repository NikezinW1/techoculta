import os
import re
import glob

BLOG_DIR = r"e:\ofertas_telegram\blog_de_ofertas\tender-trappist\src\content\blog"

files = glob.glob(os.path.join(BLOG_DIR, "*.mdx"))

# Sort files alphabetically or by cluster for a natural timeline
files.sort()

# Today is 2026-08-09. 7 days ago is 2026-08-02.
# We have 36 files. Assigning ~4 to 5 articles per day across the 8 days (Aug 02 to Aug 09).
# Let's map dates explicitly:

# Available dates: 2026-08-02 to 2026-08-09
dates = [
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
    # Distribute evenly across the 8 available days
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

print("SUCCESS: All article pubDates updated to the last 7 days (2026-08-02 to 2026-08-09).")
