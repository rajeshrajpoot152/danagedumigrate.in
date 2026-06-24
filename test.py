from bs4 import BeautifulSoup
html = '''<div class="the_content_wrapper"><div class="vc_row"><h2>Title</h2><p><span>Hello</span> <b>World</b></p><img src="a.jpg"></div></div>'''
soup = BeautifulSoup(html, 'html.parser')
wrapper = soup.find('div')

valid_tags = ['h2', 'p', 'b', 'img']
while True:
    invalid_tag = None
    for tag in wrapper.find_all(True):
        if tag.name not in valid_tags:
            invalid_tag = tag
            break
    if not invalid_tag:
        break
    invalid_tag.unwrap()

print(str(wrapper))
