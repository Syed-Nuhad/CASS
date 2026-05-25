import os

filepath = "d:/Work/new_msg/templates/dashboard.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Tabs and Table Row Unread State
tabs_html = """
    <style>
        .dash-tabs { display: flex; gap: 12px; margin-bottom: 20px; border-bottom: 2px solid var(--border-color); overflow-x: auto; }
        .dash-tab { padding: 10px 20px; font-weight: 600; color: var(--text-muted); cursor: pointer; border-bottom: 3px solid transparent; margin-bottom: -2px; white-space: nowrap; }
        .dash-tab.active { color: #38bdf8; border-bottom-color: #38bdf8; }
        .row-unread { background: rgba(56, 189, 248, 0.05); }
    </style>
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h2 style="margin: 0; display: flex; align-items: center; gap: 10px;">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m16 6-4 4-4-4"/><path d="M16 18a4 4 0 0 0-8 0"/></svg>
            Water Delivery Queue
        </h2>
    </div>
    
    <div class="dash-tabs">
        <div class="dash-tab active">All Requests</div>
        <div class="dash-tab">Requires Action (Pending)</div>
        <div class="dash-tab">Completed</div>
    </div>
"""

content = content.replace("""    <h2>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m16 6-4 4-4-4"/><path d="M16 18a4 4 0 0 0-8 0"/></svg>
        Water Delivery Queue
    </h2>""", tabs_html)

# 2. Add visual anchor to resident and Unread class to tr
old_tr = """            <tr>
                <td style="color: var(--text-muted);">#{{ req.id|stringformat:"04d" }}</td>
                <td style="font-weight: 500;">{{ req.resident.username }}</td>"""

new_tr = """            <tr class="{% if req.status == 'PENDING' %}row-unread{% endif %}">
                <td style="color: var(--text-muted);">
                    {% if req.status == 'PENDING' %}<div style="width: 8px; height: 8px; background: #38bdf8; border-radius: 50%; display: inline-block; margin-right: 4px; box-shadow: 0 0 8px rgba(56,189,248,0.8);"></div>{% endif %}
                    #{{ req.id|stringformat:"04d" }}
                </td>
                <td style="font-weight: 500;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 28px; height: 28px; border-radius: 8px; background: #e2e8f0; color: #475569; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold;">{{ req.resident.username|make_list|first|upper }}</div>
                        {{ req.resident.username }}
                    </div>
                </td>"""

content = content.replace(old_tr, new_tr)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated dashboard.html")
