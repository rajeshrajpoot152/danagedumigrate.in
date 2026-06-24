import glob
import re

html_files = glob.glob('*.html')
errors = []
fixes_applied = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    modified = False

    # 1. Viewport Meta Check
    if '<meta name="viewport"' not in html:
        errors.append(f"[{file}] Missing viewport meta tag! Mobile UI will be broken.")

    # 2. Add 'break-words' to global typography to prevent long words from causing horizontal scroll
    if file != 'index.html':
        # Since I added 'break-words' to typography earlier? No I didn't.
        # Let's add it dynamically to the <style> block if not present
        if 'break-words' not in html and '/* Global Responsive Typography' in html:
            html = html.replace('main h1 { @apply', 'main h1 { @apply break-words')
            html = html.replace('main h2 { @apply', 'main h2 { @apply break-words')
            html = html.replace('main h3 { @apply', 'main h3 { @apply break-words')
            modified = True

    # 3. Check for any remaining absolute widths in inline styles (that I might have missed earlier)
    # E.g. width: 800px;
    if re.search(r'width\s*:\s*\d{3,}px', html):
        errors.append(f"[{file}] Warning: Found large hardcoded width in inline style.")
        # Attempt to strip it
        html = re.sub(r'width\s*:\s*\d{3,}px;?', '', html)
        modified = True

    # 4. Check for unclosed divs or generic HTML structure issues
    div_open = html.count('<div')
    div_close = html.count('</div')
    if div_open != div_close:
        errors.append(f"[{file}] Warning: div mismatch (Open: {div_open}, Close: {div_close}). This could break the layout.")

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(html)
        fixes_applied += 1

if errors:
    print("Found UI/Structure Warnings:")
    for err in errors:
        print(err)
else:
    print("All pages passed the structural and responsive UI validation flawlessly.")
    
print(f"Applied additional mobile overflow protections to {fixes_applied} files.")
