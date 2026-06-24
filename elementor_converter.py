import sys
import urllib.request
import re
from bs4 import BeautifulSoup
import traceback

def clean_element(tag):
    """Recursively strip elementor classes and divs, leaving clean semantic HTML."""
    if not hasattr(tag, 'name') or tag.name is None:
        return str(tag)
        
    # Valid tags we want to keep
    valid_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'img', 'ul', 'ol', 'li', 'strong', 'b', 'i', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
    
    # If it's a valid tag, clean its attributes and process children
    if tag.name in valid_tags:
        # Keep href and src
        attrs = {}
        if tag.has_attr('href'): attrs['href'] = tag['href']
        if tag.has_attr('src'): attrs['src'] = tag['src']
        if tag.has_attr('alt'): attrs['alt'] = tag['alt']
        
        # Build clean tag
        html = f"<{tag.name}"
        for k, v in attrs.items():
            html += f' {k}="{v}"'
        
        # Void elements
        if tag.name in ['img', 'br']:
            return html + "/>"
            
        html += ">"
        for child in tag.contents:
            html += clean_element(child)
        html += f"</{tag.name}>"
        return html
        
    # If it's a div, span, etc., just unwrap it and process children
    html = ""
    for child in tag.contents:
        html += clean_element(child)
    return html

def process_page(filename):
    print(f"Processing {filename}...")
    
    # Deduce URL
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
    
    # Find the elementor wrapper
    elementor_wrapper = live_soup.find('div', {'data-elementor-type': 'wp-page'}) or live_soup.find('div', class_='elementor')
    if not elementor_wrapper:
        print("Could not find elementor wrapper in live site!")
        return False
        
    sections = elementor_wrapper.find_all('section', class_=re.compile(r'elementor-section'), recursive=False)
    
    if not sections:
        # Sometimes sections are wrapped in an inner div
        inner = elementor_wrapper.find('div', class_='elementor-inner')
        if inner:
            sections = inner.find_all('section', class_=re.compile(r'elementor-section'), recursive=False)
    
    print(f"Found {len(sections)} top-level sections.")
    
    new_main_content = ""
    
    for i, section in enumerate(sections):
        # Determine number of columns
        # In Elementor, columns are usually direct children of .elementor-container -> .elementor-row (older) or just direct
        container = section.find('div', class_=re.compile(r'elementor-container'))
        if not container:
            continue
            
        columns = container.find_all('div', class_=re.compile(r'elementor-column'), recursive=False)
        if not columns:
            # Maybe inside an elementor-row
            row = container.find('div', class_='elementor-row')
            if row:
                columns = row.find_all('div', class_=re.compile(r'elementor-column'), recursive=False)
                
        num_cols = len(columns)
        if num_cols == 0:
            continue
            
        # Is this a Hero section? (Usually the first section, has an h1 or h2 and maybe a background image)
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
            # Alternating background colors for sections
            bg_color = "bg-white" if i % 2 == 1 else "bg-gray-50 border border-gray-100"
            new_main_content += f"""
            <!-- Section {i+1} -->
            <section class="{bg_color} rounded-3xl shadow-sm p-8 md:p-12 mb-12">
            """
            
        # If multiple columns, use Grid
        if num_cols > 1:
            grid_class = f"grid md:grid-cols-{num_cols} gap-8 items-center"
            new_main_content += f'<div class="{grid_class}">'
            
        # Process Columns
        for col in columns:
            if num_cols > 1:
                new_main_content += '<div class="space-y-4">'
            else:
                new_main_content += '<div class="max-w-4xl mx-auto space-y-4 text-center md:text-left">' if is_hero else '<div class="max-w-5xl mx-auto space-y-4">'
                
            # Extract content from column
            # We want to find all elementor-widget-container and extract their inner clean HTML
            widgets = col.find_all('div', class_='elementor-widget-container')
            for widget in widgets:
                clean_html = clean_element(widget)
                if clean_html.strip():
                    new_main_content += clean_html
                    
            new_main_content += '</div>' # close col
            
        if num_cols > 1:
            new_main_content += '</div>' # close grid
            
        new_main_content += '</section>' # close section
        
    if not new_main_content:
        print("Failed to generate any sections!")
        return False
        
    # Read local file and replace <main> contents
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            local_html = f.read()
            
        local_soup = BeautifulSoup(local_html, 'html.parser')
        main_tag = local_soup.find('main')
        if not main_tag:
            print("No <main> tag in local file!")
            return False
            
        main_tag.clear()
        
        # Parse new content and append
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
        print("Usage: python elementor_converter.py <filename.html>")
