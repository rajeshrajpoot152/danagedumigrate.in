import os
import glob
import re
from bs4 import BeautifulSoup

html_files = glob.glob('*.html')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Page Name from Filename
    basename = os.path.basename(file)
    name_without_ext = os.path.splitext(basename)[0]
    
    if name_without_ext.lower() == 'index':
        page_name = "Home"
        seo_title = "Danag Edumigrate | Best Study Abroad Opportunities"
    else:
        # Convert 'study-in-usa' to 'Study In Usa'
        page_name = ' '.join(word.capitalize() for word in name_without_ext.split('-'))
        seo_title = f"{page_name} | Danag Edumigrate"
        
    # 2. Fix Title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = seo_title
    else:
        new_title = soup.new_tag('title')
        new_title.string = seo_title
        if soup.head:
            soup.head.insert(0, new_title)
            
    # 3. Add Canonical Link
    canonical = soup.find('link', rel='canonical')
    if not canonical and soup.head:
        new_canonical = soup.new_tag('link')
        new_canonical['rel'] = 'canonical'
        # Adjust URL depending on if it's index or not
        url_path = '' if name_without_ext == 'index' else f"{name_without_ext}/"
        new_canonical['href'] = f"https://danagedumigrate.in/{url_path}"
        soup.head.append(new_canonical)
        
    # 4. Add Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    main_tag = soup.find('main')
    
    desc_text = f"Explore {page_name} with Danag Edumigrate. Your trusted companion for studying abroad."
    if main_tag:
        first_p = main_tag.find('p')
        if first_p and first_p.text.strip():
            desc_text = first_p.text.strip()
            # Truncate to ~155 chars
            if len(desc_text) > 155:
                desc_text = desc_text[:152] + "..."
                
    if not meta_desc and soup.head:
        new_meta = soup.new_tag('meta')
        new_meta['name'] = 'description'
        new_meta['content'] = desc_text
        soup.head.append(new_meta)
    elif meta_desc:
        meta_desc['content'] = desc_text

    # 5. Fix Headings (Exactly one H1 per page in main content)
    if main_tag:
        h1_tags = main_tag.find_all('h1')
        if len(h1_tags) == 0:
            # No H1 found. Find first H2 and convert to H1
            first_h2 = main_tag.find('h2')
            if first_h2:
                first_h2.name = 'h1'
            else:
                # No H2 either, just prepend an H1
                new_h1 = soup.new_tag('h1')
                new_h1.string = page_name
                main_tag.insert(0, new_h1)
        elif len(h1_tags) > 1:
            # Multiple H1s. Keep first, convert rest to H2
            for idx, h1 in enumerate(h1_tags):
                if idx > 0:
                    h1.name = 'h2'
                    
    # 6. Fix Alt Tags for Images
    for img in soup.find_all('img'):
        alt_text = img.get('alt', '').strip()
        src = img.get('src', '').lower()
        
        if not alt_text:
            if 'logo' in src:
                img['alt'] = "Danag Edumigrate Logo"
            else:
                # Try to use filename for alt text if possible
                img_basename = os.path.basename(src)
                img_name = os.path.splitext(img_basename)[0]
                img_name_clean = ' '.join(word.capitalize() for word in img_name.split('-') if word)
                if img_name_clean:
                    img['alt'] = f"{img_name_clean} - {page_name}"
                else:
                    img['alt'] = f"{page_name} illustration"

    # Save the modified HTML
    # We use prettify but sometimes it adds too much whitespace. 
    # Just stringifying it works to preserve the exact format but with our modifications.
    with open(file, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print(f"SEO enhancements applied to {len(html_files)} files.")
