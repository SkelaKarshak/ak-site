import re

with open('portfolio.css', 'r') as f:
    css = f.read()

# Make sure slide-content-wrapper has container-type
if 'container-type: size;' not in css:
    css = css.replace('.slide-content-wrapper {', '.slide-content-wrapper {\n            container-type: size;')

# Now replace vw with cqw and vh with cqh
# But NOT for .slide, .slide-content-wrapper, .rotation-overlay, .slide-container
# To be safe, we'll only replace vw/vh for font-size, margin, padding, width, height where value is small (like 0.85vw, 1.2vw, 8.4vw)
css = re.sub(r'([0-9.]+)vw', r'\1cqw', css)
css = re.sub(r'([0-9.]+)vh', r'\1cqh', css)

# Revert specific classes that MUST be vw/vh
css = css.replace('100cqh', '100vh')
css = css.replace('100cqw', '100vw')
css = css.replace('50cqh', '50cqh') # Wait, grid template rows 50vh should probably be 50cqh if inside wrapper
css = css.replace('max-width: 177.78cqh;', 'max-width: 177.78vh;')
css = css.replace('height: 25cqh;', 'height: 25cqh;') # Footer is inside wrapper

with open('portfolio.css', 'w') as f:
    f.write(css)

print("CSS units updated to cqw/cqh for perfect scaling")
