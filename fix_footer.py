import os
import re

auth_files = [
    'login.html',
    'register.html',
    'driver_login.html',
    'driver_register.html',
    'staff_login.html',
    'staff_create.html'
]

base_dir = 'd:/Work/new_msg/templates'

for filename in auth_files:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove justify-content and align-items from body so they don't squish full-width elements
    content = re.sub(r'justify-content:\s*center;\n?', '', content)
    content = re.sub(r'align-items:\s*center;\n?', '', content, count=1) # only in body, wait, regex might match others.
    
    # Better: explicitly replace body { ... }
    body_match = re.search(r'body\s*\{([^}]*)\}', content)
    if body_match:
        body_rules = body_match.group(1)
        body_rules = re.sub(r'justify-content:\s*center;?', '', body_rules)
        body_rules = re.sub(r'align-items:\s*center;?', '', body_rules)
        content = content[:body_match.start(1)] + body_rules + content[body_match.end(1):]

    # Find the footer div which contains 'border-top' and add width: 100%; margin-top: auto;
    # It usually starts with <div style="... border-top: 1px solid var(--border-color) ..."
    # Let's replace 'margin-top: 40px;' with 'margin-top: auto;'
    content = content.replace('margin-top: 40px; background: rgba(0,0,0,0.02);', 'margin-top: auto; background: rgba(0,0,0,0.02);')
    
    # Add width: 100%; if not present
    if 'width: 100%;' not in content[content.rfind('border-top'):]:
        # we can just blindly add width: 100%; to the footer inline style
        content = re.sub(r'(border-top:\s*1px solid var\(--border-color\);)', r'\1 width: 100%;', content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Footers fixed.")
