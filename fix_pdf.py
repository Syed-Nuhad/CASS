import os

# 1. Update views.py
views_path = "d:/Work/new_msg/services/views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

old_pdf_logic = """    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 140, "Current Month Summary")
    
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 160, f"Total Income: ${monthly_income}")
    p.drawString(50, height - 180, f"Total Expenses: ${monthly_expenses}")
    p.drawString(50, height - 200, f"Net Profit: ${monthly_profit}")
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 250, "Annual Breakdown")
    
    y = height - 280
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Month")
    p.drawString(150, y, "Income")
    p.drawString(250, y, "Expenses")
    p.drawString(350, y, "Profit")
    
    y -= 20
    p.setFont("Helvetica", 10)
    for row in annual_data:
        if y < 50:
            p.showPage()
            y = height - 50
        
        p.drawString(50, y, row['month'])
        p.drawString(150, y, f"${row['income']}")
        p.drawString(250, y, f"${row['expense']}")
        p.drawString(350, y, f"${row['profit']}")
        y -= 20
        
    y -= 10
    if y < 50:
        p.showPage()
        y = height - 50
        
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Grand Total")
    p.drawString(150, y, f"${annual_total_income}")
    p.drawString(250, y, f"${annual_total_expense}")
    p.drawString(350, y, f"${annual_total_profit}")"""

new_pdf_logic = """    report_type = request.GET.get('type', 'monthly')

    if report_type == 'monthly':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, "Current Month Summary")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 160, f"Total Income: ${monthly_income}")
        p.drawString(50, height - 180, f"Total Expenses: ${monthly_expenses}")
        p.drawString(50, height - 200, f"Net Profit: ${monthly_profit}")
    elif report_type == 'annual':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, "Annual Breakdown")
        
        y = height - 170
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Month")
        p.drawString(150, y, "Income")
        p.drawString(250, y, "Expenses")
        p.drawString(350, y, "Profit")
        
        y -= 20
        p.setFont("Helvetica", 10)
        for row in annual_data:
            if y < 50:
                p.showPage()
                y = height - 50
            
            p.drawString(50, y, row['month'])
            p.drawString(150, y, f"${row['income']}")
            p.drawString(250, y, f"${row['expense']}")
            p.drawString(350, y, f"${row['profit']}")
            y -= 20
            
        y -= 10
        if y < 50:
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Grand Total")
        p.drawString(150, y, f"${annual_total_income}")
        p.drawString(250, y, f"${annual_total_expense}")
        p.drawString(350, y, f"${annual_total_profit}")"""

views_content = views_content.replace(old_pdf_logic, new_pdf_logic)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)


# 2. Update accounts_dashboard.html
html_path = "d:/Work/new_msg/templates/accounts_dashboard.html"
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace button
html_content = html_content.replace(
    '<a href="{% url \'export_financial_pdf\' %}" class="btn-action btn-print">Save PDF Report</a>',
    '<a id="pdf-export-link" href="{% url \'export_financial_pdf\' %}?type=monthly" class="btn-action btn-print">Save Monthly PDF</a>'
)

# Update Javascript
old_js = """        <script>
            function switchTab(tabId, btn) {
                // Update buttons
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update content
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.getElementById(tabId + '-tab').classList.add('active');
            }
        </script>"""

new_js = """        <script>
            function switchTab(tabId, btn) {
                // Update buttons
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update content
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.getElementById(tabId + '-tab').classList.add('active');
                
                // Update PDF link dynamically
                const pdfLink = document.getElementById('pdf-export-link');
                if (pdfLink) {
                    pdfLink.href = "{% url 'export_financial_pdf' %}?type=" + tabId;
                    pdfLink.innerText = "Save " + (tabId === 'monthly' ? "Monthly" : "Annual") + " PDF";
                }
            }
        </script>"""

html_content = html_content.replace(old_js, new_js)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated views.py and accounts_dashboard.html")
