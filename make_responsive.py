import re

# --- Update base.html ---
base_path = "d:/Work/new_msg/templates/base.html"
with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

# Add responsive CSS to base.html
responsive_css = """
        /* Responsive Mobile Layout */
        .mobile-menu-btn {
            display: none;
            background: none;
            border: none;
            color: var(--primary-glow);
            cursor: pointer;
            padding: 8px;
            margin-right: 15px;
        }
        
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }

        @media (max-width: 768px) {
            .mobile-menu-btn {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .sidebar {
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                box-shadow: 4px 0 20px rgba(0,0,0,0.1);
            }
            .sidebar.active {
                transform: translateX(0);
            }
            
            .main-content {
                margin-left: 0;
                padding: 20px 15px;
            }
            
            .header {
                padding: 15px 20px;
                border-radius: 12px;
                margin-bottom: 25px;
                justify-content: flex-start;
                gap: 15px;
            }
            
            .header-right {
                margin-left: auto;
            }
            
            .header h1 {
                font-size: 20px;
            }
            
            .user-profile span {
                display: none; /* Hide username text on mobile */
            }
            
            .card {
                padding: 20px;
            }
        }
    </style>
"""
base_content = base_content.replace('    </style>', responsive_css)

# Add Hamburger Menu Button
hamburger_svg = """<button class="mobile-menu-btn" onclick="document.querySelector('.sidebar').classList.toggle('active')">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
            </button>
            <h1>"""
base_content = base_content.replace('<h1>', hamburger_svg, 1)

# Group user-profile to header-right for flex
base_content = base_content.replace('<div class="user-profile">', '<div class="header-right"><div class="user-profile">')
base_content = base_content.replace('</div>\n        </div>\n\n        {% block content %}', '</div></div>\n        </div>\n\n        {% block content %}')

# Let's fix the header flex in base.html specifically:
# Right now it's:
#         <div class="header">
#             <h1>Dashboard</h1>
#             <div class="user-profile">...</div>
#         </div>

header_match = re.search(r'(<div class="header">.*?<div class="user-profile">.*?</div>\n\s*</div>)', base_content, re.DOTALL)
if header_match:
    old_header = header_match.group(1)
    new_header = old_header.replace('<div class="user-profile">', '<div class="header-right" style="display:flex; gap:15px; align-items:center;"><div class="user-profile">')
    # add the closing div for header-right
    new_header = new_header.replace('</a>\n            </div>', '</a>\n            </div></div>')
    base_content = base_content.replace(old_header, new_header)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(base_content)


# --- Update dashboard.html ---
dash_path = "d:/Work/new_msg/templates/dashboard.html"
with open(dash_path, 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Wrap tables
dash_content = dash_content.replace('<table>', '<div class="table-responsive">\n        <table>')
dash_content = dash_content.replace('</table>', '</table>\n        </div>')

# Ensure action buttons wrap
dash_content = dash_content.replace('<div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 20px; gap: 12px;">', '<div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 20px; gap: 12px; flex-wrap: wrap;">')

with open(dash_path, 'w', encoding='utf-8') as f:
    f.write(dash_content)


# --- Update accounts_dashboard.html ---
acc_path = "d:/Work/new_msg/templates/accounts_dashboard.html"
with open(acc_path, 'r', encoding='utf-8') as f:
    acc_content = f.read()

acc_content = acc_content.replace('<table>', '<div style="overflow-x: auto; width: 100%;">\n        <table>')
acc_content = acc_content.replace('</table>', '</table>\n        </div>')

with open(acc_path, 'w', encoding='utf-8') as f:
    f.write(acc_content)

print("Applied responsive refactor")
