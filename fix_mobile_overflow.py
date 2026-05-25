import re

filepath = "d:/Work/new_msg/templates/base.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add overflow-x: hidden to body
body_target = "            min-height: 100vh;\n        }"
body_replacement = "            min-height: 100vh;\n            overflow-x: hidden;\n        }"
content = content.replace(body_target, body_replacement)

# 2. Add .footer-main CSS
footer_css_target = "        /* Main Content Area */"
footer_css_replacement = "        .footer-main { margin-left: -40px; margin-right: -40px; margin-bottom: -40px; }\n        /* Main Content Area */"
content = content.replace(footer_css_target, footer_css_replacement)

# 3. Add mobile footer CSS
mobile_css_target = "            .card {\n                padding: 20px;\n            }"
mobile_css_replacement = "            .card {\n                padding: 20px;\n            }\n            .footer-main {\n                margin-left: -15px;\n                margin-right: -15px;\n                margin-bottom: -20px;\n            }"
content = content.replace(mobile_css_target, mobile_css_replacement)

# 4. Remove inline margins from footer
inline_footer_target = 'margin-top: auto; margin-left: -40px; margin-right: -40px; margin-bottom: -40px; background: rgba(0,0,0,0.02);'
inline_footer_replacement = 'margin-top: auto; background: rgba(0,0,0,0.02);'
content = content.replace(inline_footer_target, inline_footer_replacement)

# 5. Add class to footer
footer_tag_target = '<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 40px; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--border-color); margin-top: auto; background: rgba(0,0,0,0.02);">'
footer_tag_replacement = '<div class="footer-main" style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 40px; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--border-color); margin-top: auto; background: rgba(0,0,0,0.02);">'
content = content.replace(footer_tag_target, footer_tag_replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed mobile overflow")
