import os
import re

footer_html = """    <div style="background: var(--primary, #191970); color: rgba(255,255,255,0.8); padding: 40px 30px; font-size: 13px; margin-top: 60px; border-radius: 16px 16px 0 0; display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: 24px; box-shadow: 0 -10px 40px rgba(0,0,0,0.1);">
        {% if system_settings and system_settings.branding_logo %}
        <div style="background: white; padding: 10px; border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
            <img src="{{ system_settings.branding_logo.url }}" alt="Organization Logo" style="height: 48px; object-fit: contain;">
        </div>
        {% endif %}
        <div style="text-align: left; line-height: 1.6;">
            {% if system_settings %}
                {% if system_settings.company_address %}<div style="font-weight: 600; color: white; font-size: 16px; margin-bottom: 6px;">{{ system_settings.company_address }}</div>{% endif %}
                <div style="display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 8px; font-weight: 500;">
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
            <div style="opacity: 0.6;">&copy; {% now "Y" %} CASS. All rights reserved.</div>
        </div>
    </div>"""

directory = "d:/Work/new_msg/templates/"

# We want to replace the current footer div block.
# We will match from <div style="display: flex;... border-top: 1px solid var(--border-color); margin-top: 40px;"> down to the closing </div>
# Since there are multiple divs, we use regex carefully.
old_style_regex = r'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start; gap: \d+px; padding: \d+px[^;]*; color: var\(--text-muted\); font-size: 13px; border-top: 1px solid var\(--border-color\); margin-top: 40px;">[\s\S]*?&copy;[\s\S]*?</div>\s*</div>'

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # We need a robust regex to find the entire footer block we just wrote in the previous step.
        # It starts with `<div style="display: flex; flex-wrap: wrap;` and ends after the `&copy;` part.
        match = re.search(r'<div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: flex-start;[^>]*>.*?&copy;.*?</div>\s*</div>', content, re.DOTALL)
        
        if match:
            new_content = content[:match.start()] + footer_html + content[match.end():]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("Updated dark footer in", filename)
