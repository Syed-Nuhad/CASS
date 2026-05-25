import os
import re

filepath = "d:/Work/new_msg/templates/accounts_dashboard.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update body and .container CSS
css_old = """        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            background-color: var(--bg-color);
            color: var(--text-main);
            padding: 40px 20px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
        }"""

css_new = """        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            width: 100%;
            padding: 40px 20px;
            flex: 1;
            box-sizing: border-box;
        }"""
content = content.replace(css_old, css_new)

# 2. Extract the footer and move it outside the container
footer_regex = re.compile(r'(\s*<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 20px; color: var\(--text-muted\); font-size: 13px; border-top: 1px solid var\(--border-color\); margin-top: 40px; background: rgba\(0,0,0,0\.02\);">.*?</div>\s*</div>\s*</div>\s*</div>\s*</body>)', re.DOTALL)

match = footer_regex.search(content)
if match:
    footer_code = match.group(0)
    # The footer code currently contains the closing tags for the container
    # Let's rebuild the bottom of the file cleanly
    
    # First, find the real footer content (from `<div style="display...` to its closing `</div>`)
    inner_footer_match = re.search(r'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 20px; color: var\(--text-muted\); font-size: 13px; border-top: 1px solid var\(--border-color\); margin-top: 40px; background: rgba\(0,0,0,0\.02\);">.*?(?<=All rights reserved\.</div>\n        </div>\n    </div>)', footer_code, re.DOTALL)
    
    if inner_footer_match:
        actual_footer = inner_footer_match.group(0)
        
        # Modify the footer's padding to align with the max-width container, and set margin-top: auto
        # We also remove the margin-top: 40px because we want it sticky at the bottom
        actual_footer = actual_footer.replace('padding: 30px 20px;', 'padding: 30px calc(50vw - 500px); box-sizing: border-box; width: 100%;')
        actual_footer = actual_footer.replace('margin-top: 40px;', 'margin-top: auto;')
        
        # In case the screen is smaller than 1000px, padding: 30px 20px is safer. We can use CSS max()
        actual_footer = actual_footer.replace('padding: 30px calc(50vw - 500px);', 'padding: 30px max(20px, calc(50vw - 500px));')
        
        new_bottom = f"""
    </div> <!-- End .container -->
    
    {actual_footer}
</body>
"""
        content = content.replace(footer_code, new_bottom)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated accounts_dashboard.html")
