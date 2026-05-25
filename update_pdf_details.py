import os

views_path = "d:/Work/new_msg/services/views.py"
with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

old_monthly_logic = """    if report_type == 'monthly':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, f"{calendar.month_name[now.month]} Summary")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 160, f"Total Income: ${monthly_income}")
        p.drawString(50, height - 180, f"Total Expenses: ${monthly_expenses}")
        p.drawString(50, height - 200, f"Net Profit: ${monthly_profit}")"""

new_monthly_logic = """    if report_type == 'monthly':
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, height - 140, f"{calendar.month_name[now.month]} Summary")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 160, f"Total Income: ${monthly_income}")
        p.drawString(50, height - 180, f"Total Expenses: ${monthly_expenses}")
        p.drawString(50, height - 200, f"Net Profit: ${monthly_profit}")
        
        expenses_list = Expense.objects.filter(date__year=now.year, date__month=now.month).order_by('-date')
        income_list = WaterRequest.objects.filter(status='DELIVERED', updated_at__year=now.year, updated_at__month=now.month).order_by('-updated_at')
        
        y = height - 240
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Company Expenses")
        
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Description")
        p.drawString(250, y, "Date")
        p.drawString(400, y, "Amount")
        
        y -= 20
        p.setFont("Helvetica", 10)
        if not expenses_list:
            p.drawString(50, y, "No expenses recorded this month.")
            y -= 20
        else:
            for exp in expenses_list:
                if y < 50:
                    p.showPage()
                    y = height - 50
                p.drawString(50, y, exp.description[:40])
                p.drawString(250, y, exp.date.strftime("%b %d, %Y"))
                p.drawString(400, y, f"-${exp.amount}")
                y -= 20
        
        y -= 20
        if y < 100:
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Delivery Revenue")
        
        y -= 20
        p.setFont("Helvetica-Bold", 10)
        p.drawString(50, y, "Order ID")
        p.drawString(250, y, "Date/Time")
        p.drawString(400, y, "Amount")
        
        y -= 20
        p.setFont("Helvetica", 10)
        if not income_list:
            p.drawString(50, y, "No revenue recorded this month.")
            y -= 20
        else:
            for inc in income_list:
                if y < 50:
                    p.showPage()
                    y = height - 50
                p.drawString(50, y, f"#{inc.id:04d}")
                p.drawString(250, y, inc.updated_at.strftime("%b %d, %H:%M"))
                p.drawString(400, y, f"+${inc.cost}")
                y -= 20"""

views_content = views_content.replace(old_monthly_logic, new_monthly_logic)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

print("Updated views.py with detailed itemized lists.")
