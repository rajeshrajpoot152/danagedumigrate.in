import urllib.request
from bs4 import BeautifulSoup
import re

def fetch_and_sectionize(slug):
    url = f"https://danagedumigrate.in/{slug}/"
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    live_html = response.read().decode('utf-8')
    soup = BeautifulSoup(live_html, 'html.parser')
    
    # In Betheme, the main content is usually inside #Content or .the_content
    content_area = soup.find(id='Content') or soup.find('div', class_='the_content')
    if not content_area:
        print("Could not find Content area!")
        return
        
    # Extract ALL meaningful tags in order to avoid nesting hell
    # We will walk the DOM tree and yield valid tags
    valid_elements = []
    
    def extract_elements(node):
        if not hasattr(node, 'name') or node.name is None:
            return
        if node.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'img', 'table']:
            # For p tags, ignore if they are empty
            text = node.get_text(strip=True)
            if node.name == 'img' or text or node.find('img'):
                # Clean the tag
                clean_node = BeautifulSoup(f"<{node.name}></{node.name}>", 'html.parser').find(node.name)
                clean_node.string = text if node.name != 'img' and not node.find('img') else ""
                
                # If it's a list, recreate the li items
                if node.name in ['ul', 'ol']:
                    for li in node.find_all('li'):
                        new_li = soup.new_tag('li')
                        # Keep links inside li
                        for a in li.find_all('a'):
                            new_a = soup.new_tag('a', href=a.get('href', '#'))
                            new_a.string = a.get_text()
                            a.replace_with(new_a)
                        new_li.append(li.get_text(strip=True)) # Simplified, losing inner HTML for now. 
                        # Actually let's just use decode_contents
                        new_li = BeautifulSoup(f"<li>{li.decode_contents()}</li>", 'html.parser').find('li')
                        clean_node.append(new_li)
                
                # If image, copy src and alt
                if node.name == 'img':
                    clean_node['src'] = node.get('src', '')
                    clean_node['alt'] = node.get('alt', '')
                    
                # If it has a link inside, keep it (like in p tags)
                if node.name == 'p' and node.find('a'):
                    clean_node = BeautifulSoup(f"<p>{node.decode_contents()}</p>", 'html.parser').find('p')
                    
                valid_elements.append(clean_node)
            return # Don't dive deeper if we found a top-level block element
            
        for child in node.children:
            extract_elements(child)
            
    extract_elements(content_area)
    
    print(f"Extracted {len(valid_elements)} semantic elements.")
    
    # Now group elements into sections based on H2
    sections = []
    current_section = []
    
    for el in valid_elements:
        if el.name in ['h1', 'h2'] and current_section:
            sections.append(current_section)
            current_section = [el]
        else:
            current_section.append(el)
            
    if current_section:
        sections.append(current_section)
        
    print(f"Grouped into {len(sections)} sections.")
    
    # Build HTML
    new_html = ""
    for i, sec in enumerate(sections):
        if not sec: continue
        
        is_hero = (i == 0)
        bg_color = "bg-white" if i % 2 == 1 else "bg-gray-50 border border-gray-100"
        
        if is_hero:
            new_html += f"""
            <!-- Section {i+1}: Hero -->
            <section class="bg-dark-purple text-white py-16 md:py-24 mb-16 rounded-[2rem] shadow-lg relative overflow-hidden mt-[-2rem] sm:mt-0">
                <div class="absolute inset-0 bg-primary/20 pattern-dots"></div>
                <div class="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full mix-blend-screen filter blur-3xl opacity-30 transform translate-x-1/2 -translate-y-1/2"></div>
                <div class="container mx-auto px-4 relative z-10 max-w-4xl text-center">
            """
        else:
            new_html += f"""
            <!-- Section {i+1} -->
            <section class="{bg_color} rounded-3xl shadow-sm p-8 md:p-12 mb-12 max-w-5xl mx-auto">
                <div class="space-y-4">
            """
            
        for el in sec:
            new_html += str(el) + "\n"
            
        if is_hero:
            new_html += "</div></section>"
        else:
            new_html += "</div></section>"
            
    # Inject into local file
    filename = f"{slug}.html"
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            local_html = f.read()
            
        local_soup = BeautifulSoup(local_html, 'html.parser')
        main_tag = local_soup.find('main')
        main_tag.clear()
        
        new_soup = BeautifulSoup(new_html, 'html.parser')
        for el in new_soup:
            main_tag.append(el)
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(local_soup))
            
        print(f"Successfully restored and sectionized {filename}!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_sectionize("study-in-usa")
