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
                    {% if system_settings.company_email %}
                    <span style="display: flex; align-items: center; gap: 6px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
                        {{ system_settings.company_email }}
                    </span>
                    {% endif %}
                    {% if system_settings.company_phone %}
                    <span style="display: flex; align-items: center; gap: 6px;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                        {{ system_settings.company_phone }}
                    </span>
                    {% endif %}
                </div>
            {% endif %}
            <div style="opacity: 0.7; margin-top: 4px;">&copy; {% now "Y" %} CASS. All rights reserved.</div>
        </div>
    </div>"""

directory = "d:/Work/new_msg/templates/"

# We will match the dark footer block we just wrote.
# Starts with <div style="background: var(--primary
# Ends after &copy; ... </div></div>
regex = r'<div style="background:\s*var\(--primary[^>]*>[\s\S]*?&copy;[\s\S]*?</div>\s*</div>'

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(regex, content)
        
        if match:
            new_content = content[:match.start()] + footer_html + content[match.end():]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Reverted footer in", filename)
