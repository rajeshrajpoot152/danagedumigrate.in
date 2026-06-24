import urllib.request
import re
import os
from html.parser import HTMLParser

class CleanHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.skip_tags = ['script', 'style', 'noscript', 'svg', 'iframe', 'header', 'footer', 'nav', 'aside', 'form', 'button']
        self.skip_level = 0
        self.in_main = False

    def handle_starttag(self, tag, attrs):
        if tag in self.skip_tags:
            self.skip_level += 1
            return
        if self.skip_level > 0:
            return
            
        # We only want to keep structural tags
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'img', 'div', 'span', 'strong', 'b', 'i', 'em', 'table', 'tr', 'td', 'th', 'tbody', 'thead']
        if tag not in allowed_tags:
            return

        # Keep only href, src, alt
        clean_attrs = []
        for k, v in attrs:
            if tag == 'a' and k == 'href':
                # Map internal links
                if v.startswith('https://danagedumigrate.in'):
                    slug = v.replace('https://danagedumigrate.in/', '')
                    if slug.endswith('/'): slug = slug[:-1]
                    slug = slug.replace('/', '-')
                    if slug == '' or slug == 'https://danagedumigrate.in':
                        v = 'index.html'
                    else:
                        v = slug + '.html'
                clean_attrs.append(f'{k}="{v}"')
            elif tag == 'img' and k in ['src', 'alt']:
                clean_attrs.append(f'{k}="{v}"')
        
        attr_str = ' ' + ' '.join(clean_attrs) if clean_attrs else ''
        self.output.append(f'<{tag}{attr_str}>')

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_level = max(0, self.skip_level - 1)
            return
        if self.skip_level > 0:
            return
            
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'div', 'span', 'strong', 'b', 'i', 'em', 'table', 'tr', 'td', 'th', 'tbody', 'thead']
        if tag in allowed_tags:
            self.output.append(f'</{tag}>')

    def handle_data(self, data):
        if self.skip_level > 0:
            return
        text = data.strip()
        if text:
            # simple escaping for < and > just in case
            text = text.replace('<', '&lt;').replace('>', '&gt;')
            self.output.append(text)

    def get_clean_html(self):
        return ''.join(self.output)

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

head_template = """<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style type="text/tailwindcss">
      @theme {{
        --color-clifford: #da373d;
      }}
    </style>
  </head>
  <body>
    <!-- Cleaned Content Starts Here -->
    {content}
  </body>
</html>"""

for filename, url in pages:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_bytes = urllib.request.urlopen(req, timeout=15).read()
        html_str = html_bytes.decode('utf-8', errors='ignore')
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', html_str, re.IGNORECASE)
        title = title_match.group(1) if title_match else "Danag Edumigrate"
        title = title.replace('&#8211;', '-').strip()
        
        # Extract body to avoid head scripts
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_str, re.IGNORECASE | re.DOTALL)
        body_content = body_match.group(1) if body_match else html_str
        
        # Clean HTML
        parser = CleanHTMLParser()
        parser.feed(body_content)
        clean_html = parser.get_clean_html()
        
        # Remove empty divs/spans that might have been left behind
        clean_html = re.sub(r'<div>\s*</div>', '', clean_html)
        clean_html = re.sub(r'<span>\s*</span>', '', clean_html)
        
        final_html = head_template.format(title=title, content=clean_html)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
            
        print(f"Cleaned and saved: {filename}")
    except Exception as e:
        print(f"Error on {filename}: {e}")
