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

media_query = """
        @media (max-width: 600px) {
            .form-row {
                flex-direction: column !important;
                gap: 0 !important;
            }
            .auth-container {
                padding: 24px !important;
                border-radius: 16px !important;
            }
            body {
                padding: 16px !important;
            }
            div[style*="border-top"] {
                padding: 20px 10px !important;
                justify-content: center !important;
                text-align: center !important;
            }
            div[style*="border-top"] > div {
                text-align: center !important;
                justify-content: center !important;
            }
        }
    </style>
"""

for filename in auth_files:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Update body rule to ensure column layout and padding
    if 'flex-direction: column;' not in content:
        content = re.sub(r'display:\s*flex;', r'display: flex;\n            flex-direction: column;\n            padding: 20px;\n            box-sizing: border-box;', content)
    
    # 2. Make auth container auto margin
    if 'margin: auto;' not in content:
        content = re.sub(r'\.auth-container\s*\{', r'.auth-container {\n            margin: auto;\n            box-sizing: border-box;', content)
        
    # 3. Add media query
    if '@media (max-width: 600px)' not in content:
        content = content.replace('</style>', media_query)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Auth CSS fixed.")
