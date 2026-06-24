import re
from bs4 import BeautifulSoup

def build_study_usa():
    # Read the existing index.html to steal the header and footer
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
        
    soup = BeautifulSoup(index_html, 'html.parser')
    
    header = str(soup.find('header'))
    footer = str(soup.find('footer'))
    head_content = str(soup.find('head')).replace('<title>Danag Edumigrate | Best Study Abroad Opportunities</title>', '<title>Study In USA | Danag Edumigrate</title>')
    
    # Text extracted from live
    hero_title = "STUDY IN USA"
    p1 = "A U.S. degree can unlock numerous opportunities, and Danag Edumigrate can guide you in gaining an international perspective, refining language skills, and enhancing career prospects. Studying abroad offers benefits such as exposure to new cultures, improved language proficiency, networking opportunities, a competitive edge in the job market, and increased self-confidence and independence. Opting for the USA as your study destination offers access to top-ranked universities, high-quality education, diverse study programs, unparalleled cultural diversity, language immersion, abundant job opportunities, financial aid options, a vibrant student life, and emphasis on safety and security."
    p2 = "Danag Edumigrate provides free counseling and guidance, assistance with the application process, support in finding financial aid, and continuous support throughout your study abroad journey. Take the first step towards your educational journey with Danag Edumigrate to explore the boundless opportunities awaiting you in the USA."
    p3 = "Understanding the process of studying in the USA can seem daunting, but Danag Edumigrate can assist in simplifying the journey. Eligibility criteria typically involve a high school diploma for undergraduate programs and a bachelor's degree for postgraduate programs, alongside English language proficiency tests like TOEFL or IELTS. Financing options include scholarships, grants, part-time work, and student loans."
    
    benefits = [
        "High Quality Education",
        "Easy & Fast student Visa Process",
        "2 years of work permit after study",
        "Permanent Residency possible after study",
        "Provide Immigration Services Experience Agents",
        "Diversity in culture and Friendly Environment"
    ]
    
    # Build main content
    main_content = f"""
    <main class="min-h-screen pb-24">
        
        <!-- Hero Section -->
        <section class="bg-dark-purple text-white pt-24 pb-32 rounded-b-[4rem] relative overflow-hidden -mt-[60px]">
            <div class="absolute inset-0 bg-primary/20 pattern-dots"></div>
            <div class="absolute top-0 right-0 w-96 h-96 bg-accent rounded-full mix-blend-screen filter blur-[100px] opacity-40 transform translate-x-1/2 -translate-y-1/2"></div>
            
            <div class="container mx-auto px-4 relative z-10 text-center max-w-4xl mt-12">
                <span class="inline-block py-1 px-3 rounded-full bg-white/10 text-accent font-semibold tracking-wider text-sm mb-6 border border-white/20">Destination Guide</span>
                <h1 class="text-5xl md:text-6xl lg:text-7xl font-extrabold mb-8 leading-tight drop-shadow-lg">{hero_title}</h1>
                <p class="text-lg md:text-xl text-gray-200 font-light max-w-3xl mx-auto leading-relaxed">
                    Unlock numerous opportunities, gain an international perspective, and enhance your career prospects with top-ranked universities.
                </p>
                <div class="mt-10">
                    <a href="contact-us.html" class="inline-block bg-accent text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-white hover:text-dark-purple hover:shadow-xl transition-all transform hover:-translate-y-1">Start Your Application</a>
                </div>
            </div>
        </section>

        <!-- Overview Section -->
        <section class="container mx-auto px-4 -mt-16 relative z-20">
            <div class="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.06)] border border-gray-100 p-8 md:p-12 lg:p-16 max-w-5xl mx-auto">
                <div class="grid lg:grid-cols-2 gap-12 items-center">
                    <div>
                        <h2 class="text-3xl font-bold text-dark-purple mb-6">Why Choose the USA?</h2>
                        <p class="text-gray-700 leading-relaxed mb-6">{p1}</p>
                        <p class="text-gray-700 leading-relaxed font-medium border-l-4 border-primary pl-4">{p2}</p>
                    </div>
                    <div class="relative">
                        <div class="absolute inset-0 bg-primary/10 rounded-2xl transform rotate-3 scale-105"></div>
                        <img src="https://danagedumigrate.in/wp-content/uploads/2023/12/How-to-Study-Abroad-after-SPM-960x628.webp" alt="Study in USA" class="relative rounded-2xl shadow-xl w-full object-cover h-[400px]">
                    </div>
                </div>
            </div>
        </section>

        <!-- Benefits Grid -->
        <section class="container mx-auto px-4 mt-24 max-w-6xl">
            <div class="text-center mb-16">
                <h2 class="text-3xl md:text-4xl font-extrabold text-dark-purple mb-4">Key Benefits of Studying in USA</h2>
                <div class="w-24 h-1 bg-accent mx-auto rounded-full"></div>
            </div>
            
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    """
    
    # SVG icons for benefits
    icons = [
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>',
        '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>'
    ]
    
    for i, b in enumerate(benefits):
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
        
    main_content += f"""
            </div>
        </section>

        <!-- Process & CTA -->
        <section class="container mx-auto px-4 mt-24">
            <div class="bg-gray-50 rounded-3xl p-8 md:p-16 max-w-5xl mx-auto border border-gray-100 flex flex-col md:flex-row items-center gap-12">
                <div class="md:w-2/3">
                    <h2 class="text-3xl font-bold text-dark-purple mb-6">Understanding the Process</h2>
                    <p class="text-gray-700 leading-relaxed text-lg">{p3}</p>
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
    
    final_html = f"""<!DOCTYPE html>
<html lang="en">
{head_content}
<body class="bg-white text-gray-800 antialiased font-sans">
{header}
{main_content}
{footer}
</body>
</html>
"""
    with open('study-in-usa.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print("Successfully built bespoke Study In USA page.")

if __name__ == "__main__":
    build_study_usa()
