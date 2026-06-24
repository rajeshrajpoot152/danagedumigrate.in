import urllib.request
from bs4 import BeautifulSoup
import re
import os
import traceback

def clean_element(tag):
    if not hasattr(tag, 'name') or tag.name is None:
        return str(tag).strip()
    return tag.get_text(strip=True)

def fetch_content_elements(url):
    print(f"Fetching {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch: {e}")
        return []
        
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try to find main content areas
    content_area = soup.find(id='Content') or soup.find('div', class_='the_content')
    if not content_area:
        content_area = soup.find('body')
        
    # We want to extract semantic blocks in order
    blocks = []
    
    # In Betheme, content is usually in .mcb-wrap or .column
    # Let's just find all headers, paragraphs, and lists directly to avoid wrapper hell
    # But we want to maintain order.
    for tag in content_area.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'img']):
        # skip header/footer/nav tags
        if tag.find_parent('header') or tag.find_parent('footer') or tag.find_parent('nav') or tag.find_parent(id='Top_bar'):
            continue
            
        if tag.name == 'img':
            src = tag.get('src', '')
            if 'logo' not in src.lower() and 'data:image' not in src:
                blocks.append({'type': 'image', 'src': src})
            continue
            
        if tag.name in ['ul', 'ol']:
            items = [li.get_text(strip=True) for li in tag.find_all('li') if len(li.get_text(strip=True)) > 2]
            if items:
                blocks.append({'type': 'list', 'items': items})
            continue
            
        text = tag.get_text(strip=True)
        # Skip empty or very short meaningless text
        if len(text) < 3:
            continue
            
        # Skip common menu text
        if text.lower() in ['home', 'contact us', 'about us', 'enquire', 'read more']:
            continue
            
        if tag.name in ['h1', 'h2', 'h3', 'h4']:
            blocks.append({'type': 'heading', 'level': tag.name, 'text': text})
        elif tag.name == 'p':
            blocks.append({'type': 'paragraph', 'text': text})
            
    return blocks

def build_beautiful_html(blocks, title=""):
    hero_title = title.replace('-', ' ').title()
    paragraphs = []
    lists = []
    images = []
    headings = []
    
    # Categorize blocks
    for b in blocks:
        if b['type'] == 'heading':
            if not hero_title or b['level'] == 'h1':
                hero_title = b['text']
            headings.append(b['text'])
        elif b['type'] == 'paragraph':
            paragraphs.append(b['text'])
        elif b['type'] == 'list':
            lists.extend(b['items'])
        elif b['type'] == 'image':
            images.append(b['src'])
            
    if not paragraphs:
        paragraphs.append("Discover boundless opportunities with Danag Edumigrate. We provide expert guidance and comprehensive services to help you achieve your goals.")
        
    main_content = f"""
    <main class="min-h-screen pb-24">
        
        <!-- Hero Section -->
        <section class="bg-dark-purple text-white pt-24 pb-32 rounded-b-[4rem] relative overflow-hidden -mt-[60px]">
            <div class="absolute inset-0 bg-primary/20 pattern-dots"></div>
            <div class="absolute top-0 right-0 w-96 h-96 bg-accent rounded-full mix-blend-screen filter blur-[100px] opacity-40 transform translate-x-1/2 -translate-y-1/2"></div>
            
            <div class="container mx-auto px-4 relative z-10 text-center max-w-4xl mt-12">
                <span class="inline-block py-1 px-3 rounded-full bg-white/10 text-accent font-semibold tracking-wider text-sm mb-6 border border-white/20">Explore Excellence</span>
                <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold mb-8 leading-tight drop-shadow-lg">{hero_title}</h1>
                <p class="text-lg md:text-xl text-gray-200 font-light max-w-3xl mx-auto leading-relaxed">
                    {paragraphs[0] if paragraphs else "Expert guidance for your journey ahead."}
                </p>
                <div class="mt-10">
                    <a href="contact-us.html" class="inline-block bg-accent text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-white hover:text-dark-purple hover:shadow-xl transition-all transform hover:-translate-y-1">Start Your Journey</a>
                </div>
            </div>
        </section>
    """

    # Section 2: Overview (Image + Text)
    img_src = images[0] if images else "https://danagedumigrate.in/wp-content/uploads/2023/12/How-to-Study-Abroad-after-SPM-960x628.webp"
    p2 = paragraphs[1] if len(paragraphs) > 1 else "Our dedicated team of professionals will ensure that your application process is smooth, fast, and successful. We believe in providing the highest quality of service."
    
    main_content += f"""
        <!-- Overview Section -->
        <section class="container mx-auto px-4 -mt-16 relative z-20">
            <div class="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.06)] border border-gray-100 p-8 md:p-12 lg:p-16 max-w-5xl mx-auto">
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div>
                        <h2 class="text-3xl font-bold text-dark-purple mb-6">{headings[1] if len(headings)>1 else "Why Choose Us?"}</h2>
                        <p class="text-gray-700 leading-relaxed mb-6">{p2}</p>
                    </div>
                    <div class="relative">
                        <div class="absolute inset-0 bg-primary/10 rounded-2xl transform rotate-3 scale-105"></div>
                        <img src="{img_src}" alt="{hero_title}" class="relative rounded-2xl shadow-xl w-full object-cover h-[300px]">
                    </div>
                </div>
            </div>
        </section>
    """

    # Section 3: Benefits Grid (if there are lists)
    icons = [
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
    ]
    
    if lists:
        # Take up to 6 items
        lists = lists[:6]
        main_content += f"""
        <!-- Benefits Grid -->
        <section class="container mx-auto px-4 mt-24 max-w-6xl">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-extrabold text-dark-purple mb-4">Key Highlights</h2>
                <div class="w-24 h-1 bg-accent mx-auto rounded-full"></div>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        """
        for i, b in enumerate(lists):
            main_content += f"""
                <div class="bg-white p-6 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-gray-50 flex items-start space-x-4">
                    <div class="flex-shrink-0 w-12 h-12 bg-primary/10 text-primary rounded-full flex items-center justify-center">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">{icons[i % len(icons)]}</svg>
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-dark-purple mt-2">{b}</h3>
                    </div>
                </div>
            """
        main_content += """
            </div>
        </section>
        """

    # Section 4: Extra text blocks (if any)
    if len(paragraphs) > 2:
        extra_content = "<div class='space-y-4'>"
        for p in paragraphs[2:]:
            extra_content += f"<p class='text-gray-700 leading-relaxed'>{p}</p>"
        extra_content += "</div>"
        
        main_content += f"""
        <!-- Detailed Information -->
        <section class="container mx-auto px-4 mt-24">
            <div class="bg-white rounded-3xl p-8 md:p-12 max-w-4xl mx-auto border border-gray-100 shadow-sm">
                <h2 class="text-3xl font-bold text-dark-purple mb-6 border-l-4 border-accent pl-4">More Information</h2>
                {extra_content}
            </div>
        </section>
        """

    # Final CTA Section
    main_content += f"""
        <!-- Process & CTA -->
        <section class="container mx-auto px-4 mt-24">
            <div class="bg-gray-50 rounded-3xl p-8 md:p-16 max-w-5xl mx-auto border border-gray-100 flex flex-col md:flex-row items-center gap-12 shadow-sm">
                <div class="md:w-2/3">
                    <h2 class="text-3xl font-bold text-dark-purple mb-6">Ready to take the next step?</h2>
                    <p class="text-gray-700 leading-relaxed text-lg">Contact our experts today for a free consultation and personalized guidance tailored to your unique profile.</p>
                </div>
                <div class="md:w-1/3 text-center md:text-right">
                    <a href="contact-us.html" class="inline-block w-full bg-primary text-white px-8 py-5 rounded-2xl font-bold text-lg hover:bg-dark-purple hover:shadow-lg transition-all border border-white/10 relative overflow-hidden group">
                        <span class="relative z-10">Get Expert Help</span>
                        <div class="absolute inset-0 bg-white/20 transform -translate-x-full group-hover:translate-x-0 transition-transform duration-300"></div>
                    </a>
                </div>
            </div>
        </section>
    </main>
    """
    
    return main_content


def process_all_pages():
    pages = [
        ('sample-page.html', 'https://danagedumigrate.in/sample-page/'),
        ('study-in-canada.html', 'https://danagedumigrate.in/study-in-canada/'),
        ('study-in-australia.html', 'https://danagedumigrate.in/study-in-australia/'),
        ('study-in-uk.html', 'https://danagedumigrate.in/study-in-uk/'),
        ('study-in-france.html', 'https://danagedumigrate.in/study-in-france/'),
        ('study-in-italy.html', 'https://danagedumigrate.in/study-in-italy/'),
        ('canada.html', 'https://danagedumigrate.in/canada/'),
        ('migrating-to-usa.html', 'https://danagedumigrate.in/migrating-to-usa/'),
        ('united-kingdom.html', 'https://danagedumigrate.in/united-kingdom/'),
        ('australia.html', 'https://danagedumigrate.in/australia/'),
        ('free-education-consultation.html', 'https://danagedumigrate.in/free-education-consultation/'),
        ('graduate-visas.html', 'https://danagedumigrate.in/graduate-visas/'),
        ('student-visa-migration.html', 'https://danagedumigrate.in/student-visa-migration/'),
        ('change-courses-with-danag.html', 'https://danagedumigrate.in/change-courses-with-danag/'),
        ('internships-programs.html', 'https://danagedumigrate.in/internships-programs/'),
        ('student-accommodation.html', 'https://danagedumigrate.in/student-accommodation/'),
        ('contact-us.html', 'https://danagedumigrate.in/contact-us/'),
        ('about-us.html', 'https://danagedumigrate.in/about-us/'),
        ('embarking-on-global-learning-adventures-uncover-the-best-study-abroad-opportunities-for-success.html', 'https://danagedumigrate.in/embarking-on-global-learning-adventures-uncover-the-best-study-abroad-opportunities-for-success/'),
        ('embark-on-your-path-to-international-excellence-unveiling-top-destinations-for-studying-abroad-in-2024.html', 'https://danagedumigrate.in/embark-on-your-path-to-international-excellence-unveiling-top-destinations-for-studying-abroad-in-2024/'),
        ('a-comprehensive-guide-to-study-abroad-programs-in-2024.html', 'https://danagedumigrate.in/a-comprehensive-guide-to-study-abroad-programs-in-2024/'),
        ('category-uncategorized.html', 'https://danagedumigrate.in/category/uncategorized/'),
        ('author-admin.html', 'https://danagedumigrate.in/author/admin/')
    ]
    
    # Read header and footer from index.html (the source of truth)
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            index_html = f.read()
        soup = BeautifulSoup(index_html, 'html.parser')
        header_html = str(soup.find('header'))
        footer_html = str(soup.find('footer'))
        head_tag = str(soup.find('head'))
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return

    for filename, url in pages:
        if not os.path.exists(filename):
            print(f"File {filename} not found, skipping.")
            continue
            
        print(f"\n--- Processing {filename} ---")
        blocks = fetch_content_elements(url)
        if not blocks:
            print("No blocks extracted, skipping.")
            continue
            
        slug = filename.replace('.html', '')
        main_content = build_beautiful_html(blocks, title=slug)
        
        # Build the final page
        # Update title
        custom_head = head_tag.replace('<title>Danag Edumigrate | Best Study Abroad Opportunities</title>', f'<title>{slug.replace("-", " ").title()} | Danag Edumigrate</title>')
        
        final_html = f"""<!DOCTYPE html>
<html lang="en">
{custom_head}
<body class="bg-white text-gray-800 antialiased font-sans">
{header_html}
{main_content}
{footer_html}
</body>
</html>
"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(final_html)
            print(f"Successfully built {filename} with smart UI!")
        except Exception as e:
            print(f"Failed to write {filename}: {e}")
            
if __name__ == "__main__":
    process_all_pages()
