import re

with open('portfolio.html', 'r') as f:
    html = f.read()

# Pattern to find all <section class="slide"...>
# We need to wrap the inside of every section class="slide" with <div class="slide-content-wrapper">
def repl(m):
    # m.group(1) is the <section...> tag
    # m.group(2) is the inner content
    # m.group(3) is </section>
    
    inner = m.group(2)
    # If it's already wrapped, skip
    if 'class="slide-content-wrapper"' in inner:
        return m.group(0)
    
    # We want to change the inner grid classes if they exist on the slide
    # Actually it's easier to just add the wrapper.
    return f"{m.group(1)}\n<div class=\"slide-content-wrapper\">\n{inner}\n</div>\n{m.group(3)}"

html = re.sub(r'(<section[^>]*class="slide[^>]*>)(.*?)(</section>)', repl, html, flags=re.DOTALL)

with open('portfolio.html', 'w') as f:
    f.write(html)

with open('portfolio.css', 'r') as f:
    css = f.read()

# We need to make .slide a flex container to center the wrapper
slide_css = """
        .slide {
            height: 100vh;
            width: 100vw;
            scroll-snap-align: start;
            scroll-snap-stop: always;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #000;
        }

        .slide-content-wrapper {
            width: 100vw;
            height: 56.25vw;
            max-height: 100vh;
            max-width: 177.78vh;
            position: relative;
            background-color: #000;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .slide-content-wrapper > .quadrant {
            position: absolute;
            width: 50%;
            height: 50%;
        }
        
        /* Position the quadrants explicitly since grid is trickier with wrapper */
        .slide-content-wrapper > .quadrant:nth-child(1) { top: 0; left: 0; }
        .slide-content-wrapper > .quadrant:nth-child(2) { top: 0; left: 50%; }
        .slide-content-wrapper > .quadrant:nth-child(3) { top: 50%; left: 0; }
        .slide-content-wrapper > .quadrant:nth-child(4) { top: 50%; left: 50%; }
"""

# Let's completely replace the old .slide block and add the wrapper block
# Also, remove the old grid logic from .slide
css = re.sub(r'\.slide\s*{[^}]*}', slide_css, css, count=1)

with open('portfolio.css', 'w') as f:
    f.write(css)

print("Done wrapping slides")
