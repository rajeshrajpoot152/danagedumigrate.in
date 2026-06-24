import urllib.request
import re
from collections import Counter

url = 'https://danagedumigrate.in/'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    
    # Try to find Elementor global colors
    globals_match = re.findall(r'--e-global-color-[a-z0-9]+:\s*(#[a-fA-F0-9]{3,6})', html)
    
    # Also find all hex colors in inline styles or style tags
    all_colors = re.findall(r'#[a-fA-F0-9]{6}\b', html)
    
    print("Elementor Global Colors:")
    print(set(globals_match))
    
    print("\nMost Common Colors:")
    counter = Counter(all_colors)
    for color, count in counter.most_common(10):
        print(f"{color}: {count}")

except Exception as e:
    print(f"Error: {e}")
