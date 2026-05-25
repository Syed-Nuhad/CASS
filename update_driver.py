import os
import re

filepath = "d:/Work/new_msg/templates/driver_app.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add styles for tabs and unread state
style_additions = """
        /* Tabs */
        .tabs-container {
            display: flex; gap: 8px; margin-bottom: 16px; margin-top: 10px;
            overflow-x: auto; padding-bottom: 4px;
        }
        .tab-btn {
            padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: 600; cursor: pointer;
            border: 1px solid var(--border-color); background: var(--surface-color); color: var(--text-muted);
            white-space: nowrap; transition: all 0.2s;
        }
        .tab-btn.active {
            background: var(--primary); color: white; border-color: var(--primary);
        }

        /* Unread State */
        .card.unread {
            background: rgba(56, 189, 248, 0.05); /* very subtle blue tint */
            border-left: 4px solid #38bdf8;
        }
        .unread-dot {
            width: 8px; height: 8px; background: #38bdf8; border-radius: 50%;
            display: inline-block; margin-right: 6px;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.8);
        }
        
        /* Card Icon Anchor */
        .card-anchor {
            width: 40px; height: 40px; border-radius: 12px; background: rgba(0,0,0,0.05);
            display: flex; align-items: center; justify-content: center;
            color: var(--primary); margin-right: 12px; flex-shrink: 0;
        }
        
        /* Inline Pill Action */
        .btn-claim, .btn-deliver {
            width: auto; padding: 10px 20px; border-radius: 24px; font-size: 13px;
            font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; gap: 6px;
            margin-top: 12px; float: right;
        }
        .card-footer {
            display: flex; justify-content: flex-end; width: 100%;
        }
"""

content = content.replace("/* Cards */", style_additions + "\n        /* Cards */")

# Modify the card structure in the HTML
card_html_old = """            <div class="card" {% if req.status == 'ON_THE_WAY' %}style="border-color: #10b981;"{% endif %}>
                <a href="{% url 'driver_order_detail' req.id %}" style="text-decoration: none; color: inherit; display: block;">
                    <div class="card-header">
                        <div>
                            <div class="card-title">{{ req.volume_liters }} Liters</div>
                            <div class="card-subtitle">{{ req.resident.username }}'s House &bull; <strong>${{ req.cost }}</strong></div>
                            <div class="card-meta">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                                {{ req.created_at|timesince }} ago
                            </div>
                        </div>
                        <div class="priority-badge priority-{{ req.priority|lower }}">
                            {{ req.get_priority_display }}
                        </div>
                    </div>
                </a>
                
                <form method="POST" action="/driver/">
                    {% csrf_token %}
                    <input type="hidden" name="request_id" value="{{ req.id }}">
                    {% if req.status == 'FORWARDED' %}
                        <input type="hidden" name="action" value="claim">
                        <button type="submit" class="btn-claim">Claim Delivery</button>
                    {% elif req.status == 'ON_THE_WAY' %}
                        <input type="hidden" name="action" value="deliver">
                        <button type="submit" class="btn-deliver">✓ Mark Delivered</button>
                    {% endif %}
                </form>
            </div>"""

card_html_new = """            <div class="card {% if req.status == 'FORWARDED' %}unread{% endif %}" {% if req.status == 'ON_THE_WAY' %}style="border-color: #10b981;"{% endif %}>
                <a href="{% url 'driver_order_detail' req.id %}" style="text-decoration: none; color: inherit; display: block;">
                    <div class="card-header" style="margin-bottom: 0;">
                        <div style="display: flex; width: 100%;">
                            <div class="card-anchor">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
                            </div>
                            <div style="flex-grow: 1;">
                                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                    <div class="card-title">
                                        {% if req.status == 'FORWARDED' %}<span class="unread-dot"></span>{% endif %}{{ req.volume_liters }} Liters
                                    </div>
                                    <div class="card-meta" style="margin-top: 0;">{{ req.created_at|date:"g:i A" }}</div>
                                </div>
                                <div class="card-subtitle">{{ req.resident.username }}'s House &bull; <strong>${{ req.cost }}</strong></div>
                            </div>
                        </div>
                    </div>
                </a>
                
                <div class="card-footer">
                    <form method="POST" action="/driver/">
                        {% csrf_token %}
                        <input type="hidden" name="request_id" value="{{ req.id }}">
                        {% if req.status == 'FORWARDED' %}
                            <input type="hidden" name="action" value="claim">
                            <button type="submit" class="btn-claim">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                                Claim Delivery
                            </button>
                        {% elif req.status == 'ON_THE_WAY' %}
                            <input type="hidden" name="action" value="deliver">
                            <button type="submit" class="btn-deliver">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 6L9 17l-5-5"/></svg>
                                Mark Delivered
                            </button>
                        {% endif %}
                    </form>
                </div>
            </div>"""

content = content.replace(card_html_old, card_html_new)

# Add tabs
tabs_html = """
            <div class="tabs-container">
                <div class="tab-btn active">Active Queue</div>
                <div class="tab-btn" onclick="window.location.href='#'">History</div>
            </div>
            <div class="section-title" style="margin-top: 10px;">Active Queue</div>"""

content = content.replace("""<div class="section-title">Active Queue</div>""", tabs_html)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated driver_app.html")
