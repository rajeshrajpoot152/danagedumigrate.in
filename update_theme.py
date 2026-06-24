import os
import glob

html_files = glob.glob('*.html')

old_style = """    <style type="text/tailwindcss">
      @theme {
        --color-clifford: #da373d;
      }
    </style>"""

new_style = """    <style type="text/tailwindcss">
      @theme {
        --color-primary: #6c3483;
        --color-secondary: #1f58ff;
        --color-accent: #0089f7;
        --color-dark-purple: #321936;
        --color-light-gray: #e2dede;
        --color-dark: #141414;
      }
    </style>"""

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(old_style, new_style)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Updated theme colors in {len(html_files)} HTML files.")
