import os
import glob
import re

html_files = glob.glob('*.html')

# Find the exact style block from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Extract style block
style_match = re.search(r'<style type="text/tailwindcss">.*?</style>', index_content, flags=re.DOTALL)
if style_match:
    style_block = style_match.group(0)
    # Extract just the CSS content
    css_content = re.sub(r'<style[^>]*>', '', style_block)
    css_content = re.sub(r'</style>', '', css_content)
    
    os.makedirs('css', exist_ok=True)
    with open('css/styles.css', 'w', encoding='utf-8') as f:
        f.write(css_content.strip())
        
# Extract script block from the end
script_match = re.search(r'<script>\s*// Mobile menu toggle.*?</script>', index_content, flags=re.DOTALL)
if script_match:
    script_block = script_match.group(0)
    js_content = re.sub(r'<script>', '', script_block)
    js_content = re.sub(r'</script>', '', js_content)
    
    os.makedirs('js', exist_ok=True)
    with open('js/script.js', 'w', encoding='utf-8') as f:
        f.write(js_content.strip())

# Replace in all files
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if style_match:
        # We'll use <style type="text/tailwindcss">@import url('css/styles.css');</style>
        # because the CDN specifically looks for type="text/tailwindcss".
        # Actually, <link rel="stylesheet" type="text/tailwindcss" href="css/styles.css" /> works in v3.
        # But wait, in V4 the new CDN uses <link rel="stylesheet" href="src/styles.css">?
        # Let's just use <link rel="stylesheet" href="css/styles.css" type="text/tailwindcss"> to be safe.
        replacement_css = '<link rel="stylesheet" type="text/tailwindcss" href="css/styles.css" />'
        # Wait, the official v4 CDN syntax is <link rel="stylesheet" href="css/styles.css" />
        # and if it has @theme, the CDN parses it. Let's stick to <style type="text/tailwindcss">@import "css/styles.css";</style>
        replacement_css = '<link rel="stylesheet" type="text/tailwindcss" href="css/styles.css" />'
        
        # Regex to replace ANY existing tailwind style block (in case it varied slightly)
        content = re.sub(r'<style type="text/tailwindcss">.*?</style>', replacement_css, content, flags=re.DOTALL)
        
    if script_match:
        replacement_js = '<script src="js/script.js" defer></script>'
        content = re.sub(r'<script>\s*// Mobile menu toggle.*?</script>', replacement_js, content, flags=re.DOTALL)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Extraction complete.")
