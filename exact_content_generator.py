import urllib.request
import re
import os

pages = [
    ('index.html', 'https://danagedumigrate.in/'),
    ('sample-page.html', 'https://danagedumigrate.in/sample-page/'),
    ('study-in-usa.html', 'https://danagedumigrate.in/study-in-usa/'),
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

def map_url_to_filename(url):
    if url == 'https://danagedumigrate.in/' or url == 'https://danagedumigrate.in':
        return 'index.html'
    
    slug = url.replace('https://danagedumigrate.in/', '')
    if slug.endswith('/'):
        slug = slug[:-1]
    
    slug = slug.replace('/', '-')
    return slug + '.html'

def fix_internal_links(html):
    def replacer(match):
        full_url = match.group(1)
        if full_url.startswith('https://danagedumigrate.in'):
            # Preserve assets like wp-content, wp-includes, etc.
            if 'wp-content' in full_url or 'wp-includes' in full_url or full_url.endswith('.jpg') or full_url.endswith('.png') or full_url.endswith('.css') or full_url.endswith('.js'):
                return f'href="{full_url}"'
            
            # Map page links to local .html files
            filename = map_url_to_filename(full_url)
            return f'href="{filename}"'
        return match.group(0)

    html = re.sub(r'href="([^"]+)"', replacer, html)
    html = re.sub(r"href='([^']+)'", replacer, html)
    return html

for filename, url in pages:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_bytes = urllib.request.urlopen(req, timeout=15).read()
        html_str = html_bytes.decode('utf-8', errors='ignore')
        
        # We process the ENTIRE HTML string now so we keep all <head> elements, CSS, meta tags, etc.
        content = fix_internal_links(html_str)
        
        # Inject Tailwind CDN right before </head> just in case we need to design later
        content = content.replace('</head>', '\n<!-- Tailwind CSS -->\n<script src="https://cdn.tailwindcss.com"></script>\n</head>')
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Generated 100% full raw HTML for: {filename}")
    except Exception as e:
        print(f"Error on {filename}: {e}")
