from bs4 import BeautifulSoup

html = '''<div class="the_content_wrapper">
    <div class="vc_row wpb_row">
        <div class="vc_col-sm-12">
            <h2>Title</h2>
            <p>Some text <span style="color:red;">with span</span></p>
            <img src="img.jpg">
            <p><span><img src="img2.jpg"></span></p>
        </div>
    </div>
</div>'''

soup = BeautifulSoup(html, 'html.parser')

invalid_tags = ['div', 'span', 'section', 'article', 'figure', 'div']
for tag_name in invalid_tags:
    for match in soup.find_all(tag_name):
        match.unwrap()

# Now strip attributes from remaining tags
for tag in soup.find_all(True):
    if tag.name == 'img':
        src = tag.get('src')
        tag.attrs = {}
        if src: tag['src'] = src
    elif tag.name == 'a':
        href = tag.get('href')
        tag.attrs = {}
        if href: tag['href'] = href
    else:
        tag.attrs = {}

print(str(soup))
