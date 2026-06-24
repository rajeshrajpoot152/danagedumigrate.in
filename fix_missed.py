import build_all_pages
import urllib.request
from bs4 import BeautifulSoup

filename = 'student-health-insurance.html'
url = 'https://danagedumigrate.in/student-health-insurance/'

print(f'Processing {filename}')
blocks = build_all_pages.fetch_content_elements(url)
if blocks:
    main_content = build_all_pages.build_beautiful_html(blocks, title='student-health-insurance')
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    soup = BeautifulSoup(index_html, 'html.parser')
    header_html = str(soup.find('header'))
    footer_html = str(soup.find('footer'))
    head_tag = str(soup.find('head'))
    custom_head = head_tag.replace('<title>Danag Edumigrate | Best Study Abroad Opportunities</title>', '<title>Student Health Insurance | Danag Edumigrate</title>')
    
    final_html = f"<!DOCTYPE html>\n<html lang=\"en\">\n{custom_head}\n<body class=\"bg-white text-gray-800 antialiased font-sans\">\n{header_html}\n{main_content}\n{footer_html}\n</body>\n</html>"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print('Done!')
