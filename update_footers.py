import os
import re

footer_html = """    <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 20px; padding: 30px 20px; color: var(--text-muted); font-size: 13px; border-top: 1px solid var(--border-color); margin-top: 40px; background: rgba(0,0,0,0.02);">
        {% if system_settings and system_settings.branding_logo %}
        <img src="{{ system_settings.branding_logo.url }}" alt="Organization Logo" style="height: 48px; object-fit: contain;">
        {% endif %}
        <div style="text-align: left; line-height: 1.6;">
            {% if system_settings %}
                {% if system_settings.company_address %}<div style="font-weight: 500; color: var(--text-main);">{{ system_settings.company_address }}</div>{% endif %}
                <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                    {% if system_settings.company_email %}<span>✉️ {{ system_settings.company_email }}</span>{% endif %}
                    {% if system_settings.company_phone %}<span>📞 {{ system_settings.company_phone }}</span>{% endif %}
                </div>
            {% endif %}
            <div style="opacity: 0.7; margin-top: 4px;">&copy; {% now "Y" %} CASS. All rights reserved.</div>
        </div>
    </div>"""

directory = "d:/Work/new_msg/templates/"
pattern = re.compile(r'<div[^>]*text-align:\s*center[^>]*>.*?\{%\s*if\s*system_settings.*?&copy;.*?</div>', re.DOTALL)

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if pattern.search(content):
            new_content = pattern.sub(footer_html, content)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Updated", filename)
