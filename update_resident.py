import os

filepath = "d:/Work/new_msg/templates/resident_app.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

style_additions = """
        /* Notification Upgrade */
        .notif-dropdown {
            max-height: 350px;
            overflow-y: auto;
            scrollbar-width: thin;
        }
        .notif-item {
            display: flex; gap: 12px; align-items: flex-start;
            padding: 16px; border-bottom: 1px solid var(--border-color);
            transition: background 0.2s;
        }
        .notif-item:hover { background: rgba(0,0,0,0.02); }
        .notif-icon {
            width: 32px; height: 32px; border-radius: 50%; background: rgba(25,25,112,0.1); color: var(--primary);
            display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 2px;
        }
        
        /* Card Icon Anchor */
        .card-anchor {
            width: 40px; height: 40px; border-radius: 12px; background: rgba(0,0,0,0.05);
            display: flex; align-items: center; justify-content: center;
            color: var(--primary); margin-right: 12px; flex-shrink: 0;
        }
"""

content = content.replace("/* Cards */", style_additions + "\n        /* Cards */")

# Refine Card UI in Resident App
card_html_old = """            <div class="card">
                <div class="card-left">
                    <div class="card-title">{{ req.volume_liters }} Liters</div>
                    <div class="card-subtitle">{{ req.created_at|date:"M d, Y" }} &bull; <strong>${{ req.cost }}</strong></div>
                </div>
                <div class="status-badge status-{{ req.status|lower }}">
                    {{ req.get_status_display }}
                </div>
            </div>"""

card_html_new = """            <div class="card" style="align-items: flex-start;">
                <div style="display: flex;">
                    <div class="card-anchor">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v8"/><path d="m4.93 10.93 1.41 1.41"/><path d="M2 18h2"/><path d="M20 18h2"/><path d="m19.07 10.93-1.41 1.41"/><path d="M22 22H2"/><path d="m16 6-4 4-4-4"/><path d="M16 18a4 4 0 0 0-8 0"/></svg>
                    </div>
                    <div class="card-left">
                        <div class="card-title">{{ req.volume_liters }} Liters</div>
                        <div class="card-subtitle">{{ req.created_at|date:"M d, Y" }} &bull; <strong>${{ req.cost }}</strong></div>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 8px;">
                    <div class="status-badge status-{{ req.status|lower }}">{{ req.get_status_display }}</div>
                    <div style="font-size: 11px; color: var(--text-muted);">{{ req.created_at|date:"g:i A" }}</div>
                </div>
            </div>"""

content = content.replace(card_html_old, card_html_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated resident_app.html")
