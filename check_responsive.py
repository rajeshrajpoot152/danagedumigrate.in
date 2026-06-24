import glob
import re
from bs4 import BeautifulSoup

html_files = glob.glob('*.html')
files_updated = 0

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    modified = False
    
    # 1. Strip hardcoded width/height that might break mobile
    for tag in soup.find_all(['img', 'table', 'iframe', 'div']):
        # If width or height is an absolute pixel value > 100 or hardcoded, it can break mobile
        if tag.has_attr('width'):
            width_val = tag['width']
            if 'px' in width_val or width_val.isdigit():
                del tag['width']
                modified = True
                
        if tag.has_attr('height'):
            height_val = tag['height']
            if 'px' in height_val or height_val.isdigit():
                del tag['height']
                modified = True
                
        # Also clean up inline styles for width
        if tag.has_attr('style'):
            style_val = tag['style']
            if 'width:' in style_val or 'height:' in style_val:
                # Remove width and height from style
                new_style = re.sub(r'(width|height)\s*:\s*[^;]+;?', '', style_val)
                if new_style.strip():
                    tag['style'] = new_style.strip()
                else:
                    del tag['style']
                modified = True

    # 2. Make Iframes (YouTube videos, etc.) responsive
    for iframe in soup.find_all('iframe'):
        parent = iframe.parent
        # Check if already wrapped
        if parent and parent.name == 'div' and 'aspect-video' in parent.get('class', []):
            continue
            
        # Wrap iframe in responsive div
        wrapper = soup.new_tag('div', attrs={'class': 'w-full aspect-video rounded-xl overflow-hidden shadow-lg my-8'})
        iframe.replace_with(wrapper)
        wrapper.append(iframe)
        # Ensure iframe itself is full size of wrapper
        iframe['class'] = iframe.get('class', []) + ['w-full', 'h-full', 'border-0']
        modified = True

    # 3. Ensure all images are responsive
    for img in soup.find_all('img'):
        # Tailwind typography in the <style> block already handles this:
        # img { @apply rounded-2xl shadow-xl my-10 max-w-full h-auto ... }
        # Just ensure they don't have conflicting inline styles (handled above)
        pass

    if modified:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        files_updated += 1

print(f"Responsiveness checked and fixed in {files_updated} files.")
