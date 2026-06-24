import os
import glob
import re
from bs4 import BeautifulSoup

html_files = glob.glob('*.html')

old_top_bar = """<div class="flex space-x-4">
                    <a href="#" class="hover:text-secondary transition">Facebook</a>
                    <a href="#" class="hover:text-secondary transition">Instagram</a>
                </div>"""

new_top_bar = """<div class="flex space-x-6 items-center">
                    <a href="https://www.facebook.com/danagedumigrate" target="_blank" class="text-white/80 hover:text-white hover:scale-110 transition-all flex items-center font-medium">
                        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.469h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.469h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg> Facebook
                    </a>
                    <a href="https://www.instagram.com/danagedumigrate/" target="_blank" class="text-white/80 hover:text-white hover:scale-110 transition-all flex items-center font-medium">
                        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg> Instagram
                    </a>
                </div>"""

# Ensure the body has the light gray background for contrast
body_regex = re.compile(r'<body([^>]*)>')

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Replace Top Bar in all files
    html_content = html_content.replace(old_top_bar, new_top_bar)
    
    # Add body background if not present
    if 'class="bg-gray-50/50 text-gray-800 antialiased"' not in html_content:
        # Check if body already has a class attribute
        if 'body class="' in html_content:
            # We assume it's clean HTML, we'll just rewrite the body tag entirely
            pass # Skipping complex regex, our generator output `<body >` or `<body>`
        html_content = re.sub(r'<body[^>]*>', '<body class="bg-gray-50/50 text-gray-800 antialiased font-sans">', html_content)
    
    # Now use BeautifulSoup for the structural changes on INNER pages only
    if file != 'index.html':
        soup = BeautifulSoup(html_content, 'html.parser')
        
        main_tag = soup.find('main')
        
        # Check if already processed (we don't want to double wrap)
        if main_tag and not soup.find(class_='bg-dark-purple text-white py-16'):
            
            # Find the H1
            h1 = main_tag.find('h1')
            h1_text = ""
            if h1:
                h1_text = h1.decode_contents() # keep any internal formatting
                h1.extract() # Remove H1 from the flow
            else:
                # Fallback to title
                title_tag = soup.find('title')
                h1_text = title_tag.text.split('|')[0].strip() if title_tag else "Page Content"

            # Check if there is an image very early on that could act as a featured image
            # We'll extract the first image if it's within the first few tags
            featured_img = None
            first_img = main_tag.find('img')
            if first_img:
                # Let's just grab its src, but we won't extract it to be safe (don't break content flow)
                # Or actually, we'll just use a solid color header, it's safer and cleaner.
                pass

            # Wrap the rest of the content
            rest_of_html = main_tag.decode_contents()
            
            # Rebuild main
            main_tag.clear()
            
            hero_html = f"""
            <!-- Premium Hero Header -->
            <section class="bg-dark-purple text-white py-16 md:py-24 mb-12 rounded-[2rem] shadow-lg relative overflow-hidden">
                <!-- Abstract Decorative Pattern -->
                <div class="absolute inset-0 opacity-10">
                    <svg class="absolute w-full h-full" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <pattern id="grid-pattern" width="40" height="40" patternUnits="userSpaceOnUse">
                                <path d="M0 40L40 0H20L0 20M40 40V20L20 40" fill="none" stroke="currentColor" stroke-width="2"/>
                            </pattern>
                        </defs>
                        <rect width="100%" height="100%" fill="url(#grid-pattern)"/>
                    </svg>
                </div>
                <div class="absolute top-0 right-0 w-96 h-96 bg-primary rounded-full mix-blend-screen filter blur-3xl opacity-30 transform translate-x-1/2 -translate-y-1/2"></div>
                <div class="absolute bottom-0 left-0 w-64 h-64 bg-secondary rounded-full mix-blend-screen filter blur-3xl opacity-20 transform -translate-x-1/2 translate-y-1/2"></div>
                
                <div class="container mx-auto px-4 relative z-10 text-center max-w-4xl">
                    <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold mb-6 leading-tight drop-shadow-md">{h1_text}</h1>
                    <div class="w-24 h-1.5 bg-accent mx-auto rounded-full mb-8 shadow-sm"></div>
                    <p class="text-lg md:text-xl text-gray-200 font-light max-w-2xl mx-auto leading-relaxed">Explore comprehensive details, insights, and opportunities tailored just for you at Danag Edumigrate.</p>
                </div>
            </section>
            
            <!-- Content Container -->
            <div class="max-w-5xl mx-auto bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.06)] border border-gray-100 p-8 md:p-12 lg:p-16 mb-24 relative z-20 -mt-16">
                {rest_of_html}
            </div>
            """
            
            # Parse the new HTML and append to main
            new_elements = BeautifulSoup(hero_html, 'html.parser')
            for el in new_elements:
                main_tag.append(el)
                
            html_content = str(soup)

    # Write back
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html_content)

print(f"Top Bar and Inner Pages upgraded across {len(html_files)} files.")
