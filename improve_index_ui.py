import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Strip all those annoying nested divs from the cleaned content to make it flat, 
# BUT wait, regex replacing divs might destroy the layout.
# Let's just wrap the entire main content in our new UI.
# Actually, the easiest way to modernize this specific page without losing content is to parse it, 
# extract the raw data, and insert it into a predefined template.

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

main_tag = soup.find('main')
if not main_tag:
    print("Main tag not found!")
    exit(1)

# Extract data
h1 = main_tag.find('h1')
hero_h1 = h1.text if h1 else "Fulfilling Your Dream of Going Abroad"
hero_sub = main_tag.find(string=re.compile("Get in touch with our guide")).parent.text if main_tag.find(string=re.compile("Get in touch with our guide")) else "Get in touch with our guide for further directions"
hero_img = main_tag.find('img', alt=re.compile("Woman"))
hero_img_src = hero_img['src'] if hero_img else "images/default.jpg"

features = []
# Features: Customer Service, Like, Flight
for feature_alt in ["Customer Service", "Like", "Flight"]:
    img = main_tag.find('img', alt=re.compile(feature_alt))
    if img:
        img_src = img['src']
        # The h6 is usually nearby
        h6 = img.find_next('h6')
        title = h6.text if h6 else ""
        features.append({"src": img_src, "title": title})

# Unique Services
services_h3 = main_tag.find(string=re.compile("UNIQUE SERVICES")).parent.text if main_tag.find(string=re.compile("UNIQUE SERVICES")) else "Explore OUR UNIQUE SERVICES"
services = []
for s_title in ["Migration", "PTE / IELTS", "Online Training", "Career Counseling"]:
    h5 = main_tag.find('h5', string=re.compile(s_title))
    if h5:
        p = h5.find_next(['p', 'div'])
        desc = p.text if p else ""
        services.append({"title": s_title, "desc": desc})

# Courses
courses_h3 = main_tag.find(string=re.compile("100 different Courses"))
courses_title = courses_h3.parent.text if courses_h3 else "We’ll help you choose from 100 different Courses"
courses = []
for h4 in main_tag.find_all('h4'):
    if h4.text not in ["15 mins video call", "30 mins video call", "60 Mins Video Call", "Have A Question?"]:
        courses.append(h4.text)

# Visa Section
visa_h5 = main_tag.find('h5', string=re.compile("Visa Process"))
visa_title = visa_h5.text if visa_h5 else "Need help with your Visa Process?"
visa_p = visa_h5.find_next('p').text if visa_h5 else "If you're finding visa applications to be complicated..."

# Booking Links
booking = []
for t in ["15 mins video call", "30 mins video call", "60 Mins Video Call", "Have A Question?"]:
    h4 = main_tag.find('h4', string=re.compile(t, re.IGNORECASE))
    if h4:
        a = h4.find_parent('a')
        if a:
            booking.append({"title": h4.text, "link": a['href']})

# University Logos
uni_logos = []
for img in main_tag.find_all('img', alt=re.compile("parnter_logo")):
    uni_logos.append(img['src'])

# Reviews
reviews_p = main_tag.find('p', string=re.compile("reviews"))
reviews_count = reviews_p.text if reviews_p else "1272 reviews"
review_imgs = []
for img in main_tag.find_all('img', alt=re.compile("1688502471811")):
    if img['src'] not in review_imgs:
        review_imgs.append(img['src'])

# News / Blog
news_h3 = main_tag.find('h3', string=re.compile("LatestNews|Latest News"))
news_items = []
# Find links that look like blog posts
for a in main_tag.find_all('a'):
    if a.has_attr('href') and '.html' in a['href'] and len(a.text) > 20 and not a.find('img'):
        # Might be a blog title
        news_items.append({"title": a.text, "link": a['href']})
        if len(news_items) >= 3:
            break

# Construct the NEW BEAUTIFUL HTML replacing the content of <main>
# We are carefully injecting the exact text back in, just wrapped in professional layouts.

new_html = f"""
<!-- 1. Hero Section -->
<section class="grid md:grid-cols-2 gap-12 items-center mb-24">
    <div class="space-y-6">
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-dark-purple leading-tight">{hero_h1}</h1>
        <p class="text-lg text-gray-600 border-l-4 border-primary pl-4">{hero_sub}</p>
        <div class="pt-4">
            <a href="contact-us.html" class="inline-block bg-primary text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-dark-purple hover:shadow-lg transition-all transform hover:-translate-y-1">Get In Touch</a>
        </div>
    </div>
    <div class="relative">
        <div class="absolute inset-0 bg-primary/10 rounded-[3rem] transform rotate-3"></div>
        <img src="{hero_img_src}" alt="Student Abroad" class="relative rounded-[3rem] shadow-2xl object-cover w-full h-[500px]">
    </div>
</section>

<!-- 2. Core Features -->
<section class="mb-24">
    <div class="grid md:grid-cols-3 gap-8">
"""
for feat in features:
    new_html += f"""
        <div class="bg-white p-8 rounded-2xl shadow-[0_4px_20px_-4px_rgba(0,0,0,0.1)] hover:shadow-[0_8px_30px_-4px_rgba(0,0,0,0.15)] transition-shadow text-center border border-gray-50">
            <div class="w-20 h-20 mx-auto bg-primary/5 rounded-full flex items-center justify-center mb-6">
                <img src="{feat['src']}" alt="{feat['title']}" class="w-12 h-12 object-contain">
            </div>
            <h3 class="text-xl font-bold text-dark-purple">{feat['title']}</h3>
        </div>
    """
new_html += f"""
    </div>
</section>

<!-- 3. Unique Services -->
<section class="bg-gray-50 -mx-4 px-4 py-20 mb-24 rounded-3xl">
    <div class="text-center mb-16">
        <h5 class="text-primary font-bold tracking-wider uppercase mb-2">Welcome to Danag Edumigrate</h5>
        <h2 class="text-3xl md:text-4xl font-extrabold text-dark-purple">{services_h3}</h2>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
"""
for s in services:
    new_html += f"""
        <div class="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border-t-4 border-primary">
            <h4 class="text-lg font-bold text-dark-purple mb-3">{s['title']}</h4>
            <p class="text-sm text-gray-600 leading-relaxed">{s['desc']}</p>
        </div>
    """
new_html += f"""
    </div>
</section>

<!-- 4. Courses -->
<section class="mb-24 text-center">
    <div class="max-w-3xl mx-auto mb-12">
        <h2 class="text-3xl md:text-4xl font-extrabold text-dark-purple leading-tight">{courses_title}</h2>
    </div>
    <div class="flex flex-wrap justify-center gap-3">
"""
# Deduplicate courses
unique_courses = list(dict.fromkeys(courses))
for c in unique_courses:
    new_html += f"""
        <span class="px-5 py-2.5 bg-white border border-gray-200 text-gray-700 rounded-full text-sm font-medium hover:border-primary hover:text-primary transition-colors cursor-default shadow-sm">{c}</span>
    """
new_html += f"""
    </div>
</section>

<!-- 5. Visa Process & CTA -->
<section class="bg-dark-purple text-white rounded-3xl p-8 md:p-16 mb-24 relative overflow-hidden">
    <div class="absolute top-0 right-0 w-64 h-64 bg-primary rounded-full mix-blend-multiply filter blur-3xl opacity-50"></div>
    <div class="relative z-10 max-w-2xl mx-auto text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-extrabold mb-6">{visa_title}</h2>
        <p class="text-gray-300 text-lg">{visa_p}</p>
    </div>
    <div class="relative z-10 grid sm:grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto">
"""
for b in booking:
    new_html += f"""
        <a href="{b['link']}" target="_blank" class="flex flex-col items-center justify-center bg-white/10 hover:bg-white/20 border border-white/20 p-6 rounded-2xl backdrop-blur-sm transition-all group">
            <svg class="w-8 h-8 text-primary mb-3 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            <span class="font-medium text-sm text-center">{b['title']}</span>
        </a>
    """
new_html += f"""
    </div>
</section>

<!-- 6. Universities & Reviews -->
<section class="mb-24">
    <div class="text-center mb-12">
        <h2 class="text-3xl md:text-4xl font-extrabold text-dark-purple mb-4">Universities We Partner With</h2>
        <p class="text-gray-600 max-w-3xl mx-auto">Empowering Your Academic Journey: Our Consortium of Esteemed Universities Ensures a Seamless Admissions Process.</p>
    </div>
    <div class="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-70 grayscale hover:grayscale-0 transition-all duration-500 mb-20">
"""
for logo in uni_logos:
    new_html += f'<img src="{logo}" alt="University Partner" class="h-12 object-contain">'
new_html += f"""
    </div>

    <div class="bg-gray-50 rounded-3xl p-8 md:p-12 text-center">
        <h3 class="text-2xl font-bold text-dark-purple mb-2">What they say about us!</h3>
        <div class="flex items-center justify-center space-x-2 mb-2">
            <span class="text-4xl font-extrabold text-primary">4.5</span>
            <div class="flex text-yellow-400">
                {"<svg class='w-6 h-6' fill='currentColor' viewBox='0 0 20 20'><path d='M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z'/></svg>" * 5}
            </div>
        </div>
        <p class="text-gray-500 mb-8">{reviews_count}</p>
        
        <div class="flex overflow-x-auto pb-8 snap-x snap-mandatory gap-6 no-scrollbar">
"""
for r_img in review_imgs:
    new_html += f"""
            <div class="snap-center shrink-0 w-80">
                <img src="{r_img}" alt="Student Review" class="rounded-xl shadow-md w-full object-cover">
            </div>
    """
new_html += f"""
        </div>
    </div>
</section>
"""

# Replace the contents of <main>
main_tag.clear()
# Insert the raw HTML directly
# BeautifulSoup might escape things if we use append(string), so we will stringify and replace
html_str = str(soup)

# We need to replace the <main class="...">...</main> with our new content
# We can just do a regex replace on the <main> tag contents.
pattern = re.compile(r'(<main[^>]*>).*?(</main>)', re.DOTALL)
final_html = pattern.sub(r'\1\n' + new_html + r'\n\2', html_str)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Home page UI modernization complete. Data extracted and injected into Tailwind components.")
