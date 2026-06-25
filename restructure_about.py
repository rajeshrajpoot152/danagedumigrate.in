import re

with open('about-us.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the global typography rules from <style> to fix the "font clear nahi dikh raha" issue.
# The style block looks like:
# <style type="text/tailwindcss">
# @theme { ... }
# /* Global Responsive Typography ... */
# main h1 { ... }
# ...
# </style>
# We want to keep only the @theme { ... } block.

style_pattern = r'(<style type="text/tailwindcss">[\s\S]*?@theme\s*{[\s\S]*?})([\s\S]*?)(</style>)'
# We replace the entire style block with just the theme part.
content = re.sub(style_pattern, r'\1\n\3', content)

# 2. Extract sections inside <div class="container mx-auto px-4 max-w-6xl mb-20">
# The structure is:
# <div class="container mx-auto px-4 max-w-6xl mb-20">
#    <!-- Introduction Section -->
#    ...
#    <!-- Counters Section -->
#    ...
#    <!-- Why Choose Us Section -->
#    ...
#    <!-- Mission, Vision, Values -->
#    ...
#    <!-- Advanced Call To Action Section -->
#    ...
# </div>

# Let's extract the main wrapper.
main_wrapper_pattern = r'<div class="container mx-auto px-4 max-w-6xl mb-20">(.*?)</div>\s*</main>'
main_wrapper_match = re.search(main_wrapper_pattern, content, re.DOTALL)

if main_wrapper_match:
    inner_html = main_wrapper_match.group(1)
    
    # Split by the comments to wrap each section in a full-width <section>
    intro = re.search(r'(<!-- Introduction Section -->.*?)(?=<!-- Counters Section -->)', inner_html, re.DOTALL).group(1)
    counters = re.search(r'(<!-- Counters Section -->.*?)(?=<!-- Why Choose Us Section -->)', inner_html, re.DOTALL).group(1)
    why_choose_us = re.search(r'(<!-- Why Choose Us Section -->.*?)(?=<!-- Mission, Vision, Values -->)', inner_html, re.DOTALL).group(1)
    mission = re.search(r'(<!-- Mission, Vision, Values -->.*?)(?=<!-- Advanced Call To Action Section -->)', inner_html, re.DOTALL).group(1)
    cta = re.search(r'(<!-- Advanced Call To Action Section -->.*)', inner_html, re.DOTALL).group(1)
    
    # Remove the rounded borders and background from Why Choose Us, as the section will handle it.
    why_choose_us = why_choose_us.replace('bg-gray-50 rounded-[3rem] p-10 md:p-16 mb-20 shadow-sm border border-gray-100', '')
    
    new_layout = f'''
    <section class="w-full py-16 bg-white">
        <div class="container mx-auto px-4 max-w-6xl">
            {intro}
        </div>
    </section>
    
    <section class="w-full py-12 bg-white relative z-10 -mt-10">
        <div class="container mx-auto px-4 max-w-6xl">
            {counters}
        </div>
    </section>
    
    <section class="w-full py-24 bg-gray-50 border-t border-b border-gray-200">
        <div class="container mx-auto px-4 max-w-6xl">
            {why_choose_us}
        </div>
    </section>
    
    <section class="w-full py-24 bg-white">
        <div class="container mx-auto px-4 max-w-6xl">
            {mission}
        </div>
    </section>
    
    <section class="w-full pt-12 pb-24 bg-white">
        <div class="container mx-auto px-4 max-w-6xl">
            {cta}
        </div>
    </section>
    </main>
    '''
    
    content = content[:main_wrapper_match.start()] + new_layout + content[main_wrapper_match.end() + 7:] # +7 for </main>

with open('about-us.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated about-us.html successfully.")
