import re

with open('/Users/aleksanderkarshikoff/Documents/ak-site/v2/portfolio.html', 'r') as f:
    html = f.read()

# 1. Extract CSS
style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
if style_match:
    css = style_match.group(1).strip()
    
    # 2. Add utility class for dark icons
    css += "\n\n/* Utility Classes */\n.icon-dark { color: #000 !important; }\n.ml-0 { margin-left: 0 !important; }\n"
    
    with open('/Users/aleksanderkarshikoff/Documents/ak-site/v2/portfolio.css', 'w') as f:
        f.write(css)
    
    html = html.replace(style_match.group(0), '<link rel="stylesheet" href="portfolio.css">')

# 3. Inject SVG sprite at the start of body
sprite = '''
    <!-- SVG Sprite for Icons -->
    <svg width="0" height="0" style="display: none;">
        <symbol id="play-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
            <polyline points="15 3 21 3 21 9" />
            <line x1="10" y1="14" x2="21" y2="3" />
        </symbol>
    </svg>
'''
html = re.sub(r'(<body>)', r'\1' + sprite, html)

# 4. Replace all inline SVGs with the <use> tag
svg_pattern = r'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">\s*<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />\s*<polyline points="15 3 21 3 21 9" />\s*<line x1="10" y1="14" x2="21" y2="3" />\s*</svg>'

# Also handle potential variations (like single line)
svg_pattern_2 = r'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" /><polyline points="15 3 21 3 21 9" /><line x1="10" y1="14" x2="21" y2="3" /></svg>'

use_tag = '<svg><use href="#play-icon-svg"></use></svg>'

html = re.sub(svg_pattern, use_tag, html, flags=re.DOTALL)
html = html.replace(svg_pattern_2.replace('\\', ''), use_tag) # just in case

# 5. Clean up inline styles
html = html.replace('style="color: #000;"', 'class="icon-dark"')
html = html.replace('class="play-icon" style="color: #000;"', 'class="play-icon icon-dark"')
html = html.replace('class="play-icon s9-play-icon" style="color: #000;"', 'class="play-icon s9-play-icon icon-dark"')
html = html.replace('style="margin-left: 0;"', 'class="ml-0"')
html = html.replace('class="play-icon" style="margin-left: 0;"', 'class="play-icon ml-0"')

with open('/Users/aleksanderkarshikoff/Documents/ak-site/v2/portfolio.html', 'w') as f:
    f.write(html)

print("Refactoring complete.")
