import re

def refactor_template(filepath, title):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract CSS
    css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    css = css_match.group(1) if css_match else ""

    # Extract Body content
    # The body content is inside <div class="container">
    # Actually, we can just grab everything inside <body> and strip out the container if we want, or keep it.
    body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
    body = body_match.group(1) if body_match else ""

    # Let's remove the <div class="container"> wrapping the body, since base.html provides .main-content
    # Wait, the body has <div class="container"> ... </div>.
    # We can just leave it, it's fine, it will just be a container inside main-content.
    # BUT, the container has a max-width and background. It's actually good for centering.
    # Let's remove the `<h1>Financial Accounts Dashboard</h1>` and its subtitle, because base.html has the header!
    # Wait, the title in base.html is just `Live Dispatch Center`. 
    # If we replace that with `{% block header_title %}` we can put the title there.
    
    # We will just inject the body inside {% block content %}

    new_content = f"""{{% extends 'base.html' %}}

{{% block header_title %}}{title}{{% endblock %}}

{{% block extra_css %}}
<style>
{css}
</style>
{{% endblock %}}

{{% block content %}}
{body}
{{% endblock %}}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

refactor_template('d:/Work/new_msg/templates/accounts_dashboard.html', 'Financial Accounts Dashboard')
refactor_template('d:/Work/new_msg/templates/staff_inventory.html', 'Inventory Control Center')

print("Refactored accounts and inventory dashboards to extend base.html")
