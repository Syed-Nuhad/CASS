import re

filepath = "d:/Work/new_msg/templates/login.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update body CSS
css_old = """        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }"""
css_new = """        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }"""
content = content.replace(css_old, css_new)

# 2. Extract footer and remove it from inside auth-container
footer_regex = re.search(r'(\s*<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 20px; color: var\(--text-muted\); font-size: 13px; border-top: 1px solid var\(--border-color\); margin-top: 40px; background: rgba\(0,0,0,0\.02\);">.*?(?<=All rights reserved\.</div>\n        </div>\n    </div>))', content, re.DOTALL)

if footer_regex:
    footer_code = footer_regex.group(1)
    # Remove footer from its current location
    content = content.replace(footer_code, "")
    
    # Format the new footer
    new_footer = footer_code.replace('padding: 30px 20px;', 'padding: 30px max(20px, calc(50vw - 500px)); width: 100%; box-sizing: border-box;')
    new_footer = new_footer.replace('margin-top: 40px;', 'margin-top: auto;')
    
    # Wrap the auth-container
    content = content.replace('<div class="auth-container">', '<div style="flex: 1; display: flex; align-items: center; justify-content: center; padding: 20px; box-sizing: border-box;">\n    <div class="auth-container">')
    
    # Close the wrapper before the footer and body tags
    # The end of the file currently is:
    #         </div>
    #     </div>
    #     </div>
    # 
    # </body>
    # Wait, the extra </div> were part of the previous script mistake on accounts, or they were just there.
    # Let's cleanly replace the end of the file.
    
    # Instead of relying on exact closing tags, we can find the end of the auth container by looking for the form closing
    
    # Wait, let's just do a regex replace to clean up the end of the file
    content = re.sub(r'\s*</div>\s*</div>\s*</div>\s*</body>', '\n    </div>\n</div>\n\n' + new_footer + '\n</body>', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated login.html layout")
