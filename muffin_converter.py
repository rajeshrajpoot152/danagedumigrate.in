import sys
import urllib.request
import re
from bs4 import BeautifulSoup
import traceback

def clean_element(tag):
    """Recursively strip muffin builder classes and divs, leaving clean semantic HTML."""
    if not hasattr(tag, 'name') or tag.name is None:
        return str(tag)
        
    valid_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li', 'strong', 'b', 'i', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
    
    if tag.name in valid_tags:
        attrs = {}
        if tag.has_attr('href'): attrs['href'] = tag['href']
        if tag.has_attr('src'): attrs['src'] = tag['src']
        if tag.has_attr('alt'): attrs['alt'] = tag['alt']
        
        html = f"<{tag.name}"
        for k, v in attrs.items():
            html += f' {k}="{v}"'
            
        if tag.name in ['img', 'br']:
            return html + "/>"
            
        html += ">"
        for child in tag.contents:
            html += clean_element(child)
        html += f"</{tag.name}>"
        return html
        
    html = ""
    for child in tag.contents:
        html += clean_element(child)
    return html

def process_page(filename):
    print(f"Processing {filename}...")
    
    slug = filename.replace('.html', '')
    url = f"https://danagedumigrate.in/{slug}/"
    if slug == "index":
        url = "https://danagedumigrate.in/"
        
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        live_html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return False
        
    live_soup = BeautifulSoup(live_html, 'html.parser')
    
    # In Muffin Builder (Betheme), sections have class 'mcb-section'
    sections = live_soup.find_all('div', class_=re.compile(r'mcb-section'))
    
    print(f"Found {len(sections)} top-level sections.")
    
    new_main_content = ""
    
    for i, section in enumerate(sections):
        # Wraps are usually columns or rows
        wraps = section.find_all('div', class_=re.compile(r'mcb-wrap'), recursive=False)
        if not wraps:
            # Maybe inside an inner div
            inner = section.find('div', class_='section_wrapper')
            if inner:
                wraps = inner.find_all('div', class_=re.compile(r'mcb-wrap'), recursive=False)
                
        num_cols = len(wraps)
        if num_cols == 0:
            continue
            
        is_hero = (i == 0)
        
        # Build Section Wrapper
        if is_hero:
            new_main_content += f"""
            <!-- Section {i+1}: Hero -->
            <section class="bg-dark-purple text-white py-16 md:py-24 mb-16 rounded-[2rem] shadow-lg relative overflow-hidden mt-[-2rem] sm:mt-0">
                <div class="absolute inset-0 bg-primary/20 pattern-dots"></div>
                <div class="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full mix-blend-screen filter blur-3xl opacity-30 transform translate-x-1/2 -translate-y-1/2"></div>
                <div class="container mx-auto px-4 relative z-10">
            """
        else:
            bg_color = "bg-white" if i % 2 == 1 else "bg-gray-50 border border-gray-100"
            new_main_content += f"""
            <!-- Section {i+1} -->
            <section class="{bg_color} rounded-3xl shadow-sm p-8 md:p-12 mb-12 max-w-6xl mx-auto">
            """
            
        if num_cols > 1:
            grid_class = f"grid md:grid-cols-{num_cols} gap-8 items-start"
            new_main_content += f'<div class="{grid_class}">'
            
        for wrap in wraps:
            if num_cols > 1:
                new_main_content += '<div class="space-y-4">'
            else:
                new_main_content += '<div class="max-w-4xl mx-auto space-y-4 text-center md:text-left">' if is_hero else '<div class="max-w-5xl mx-auto space-y-4">'
                
            items = wrap.find_all('div', class_=re.compile(r'mcb-item'))
            for item in items:
                clean_html = clean_element(item)
                if clean_html.strip():
                    new_main_content += clean_html
                    
            new_main_content += '</div>'
            
        if num_cols > 1:
            new_main_content += '</div>'
            
        new_main_content += '</section>'
        
    if not new_main_content:
        print("Failed to generate any sections!")
        return False
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            local_html = f.read()
            
        local_soup = BeautifulSoup(local_html, 'html.parser')
        main_tag = local_soup.find('main')
        if not main_tag:
            print("No <main> tag in local file!")
            return False
            
        main_tag.clear()
        new_soup = BeautifulSoup(new_main_content, 'html.parser')
        for el in new_soup:
            main_tag.append(el)
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(local_soup))
            
        print(f"Successfully converted {filename} to Tailwind Section UI!")
        return True
    except Exception as e:
        print(f"Error modifying local file: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_page(sys.argv[1])
    else:
        print("Usage: python muffin_converter.py <filename.html>")
