import os
import re

files = [
    'd:/Work/new_msg/templates/accounts_dashboard.html',
    'd:/Work/new_msg/templates/staff_inventory.html'
]

for filepath in files:
    if not os.path.exists(filepath):
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove :root { ... } block
    content = re.sub(r':root\s*\{[^}]*\}', '', content)
    
    # Remove body { ... } block
    content = re.sub(r'body\s*\{[^}]*\}', '', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Dashboards cleaned.")
