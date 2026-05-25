import re

filepath = "d:/Work/new_msg/templates/base.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add box-sizing: border-box to .card
card_css_target = "        .card { \n            background: var(--surface-color);"
card_css_replacement = "        .card { \n            box-sizing: border-box;\n            background: var(--surface-color);"
content = content.replace(card_css_target, card_css_replacement)

# 2. Hide username text on mobile
# Replace the CSS
old_hide_css = ".user-profile span {\n                display: none; /* Hide username text on mobile */\n            }"
new_hide_css = ".user-profile-text {\n                display: none;\n            }"
content = content.replace(old_hide_css, new_hide_css)

# Add the class to the HTML div
user_profile_target = """                <div>
                    <div><strong>{{ user.username }}</strong></div>
                    <div style="font-size: 12px; color: var(--text-muted);">{{ user.role }}</div>
                </div>"""
user_profile_replacement = """                <div class="user-profile-text">
                    <div><strong>{{ user.username }}</strong></div>
                    <div style="font-size: 12px; color: var(--text-muted);">{{ user.role }}</div>
                </div>"""
content = content.replace(user_profile_target, user_profile_replacement)

# 3. Add Close Button to sidebar
sidebar_header_target = """        <div style="display: flex; align-items: center; justify-content: flex-start; gap: 12px; margin-bottom: 40px; padding: 0 24px;">
            {% if system_settings and system_settings.branding_logo %}
            <img src="{{ system_settings.branding_logo.url }}" alt="CASS Logo" style="height: 40px; object-fit: contain;">
            {% endif %}
            <h2 style="margin: 0;">CASS</h2>
        </div>"""

sidebar_header_replacement = """        <div style="display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 40px; padding: 0 24px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                {% if system_settings and system_settings.branding_logo %}
                <img src="{{ system_settings.branding_logo.url }}" alt="CASS Logo" style="height: 40px; object-fit: contain;">
                {% endif %}
                <h2 style="margin: 0;">CASS</h2>
            </div>
            <button class="mobile-menu-btn" onclick="document.querySelector('.sidebar').classList.remove('active')" style="margin: 0; padding: 4px;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
        </div>"""
content = content.replace(sidebar_header_target, sidebar_header_replacement)


# Also ensure that .dash-tabs doesn't overflow .card. It has overflow-x: auto, but let's make sure its parent isn't expanding.
# Since .card now has box-sizing: border-box, it shouldn't expand.

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed mobile bugs")
