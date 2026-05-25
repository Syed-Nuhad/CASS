import os
import glob

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add box-sizing to any .container
    if '.container {' in content and 'box-sizing: border-box;' not in content.split('.container {')[1].split('}')[0]:
        content = content.replace('.container {\n', '.container {\n            box-sizing: border-box;\n            max-width: 100%;\n')

    # 2. Add box-sizing to .card
    if '.card {' in content and 'box-sizing: border-box;' not in content.split('.card {')[1].split('}')[0]:
        content = content.replace('.card {\n', '.card {\n            box-sizing: border-box;\n            max-width: 100%;\n')

    # 3. Add table-responsive CSS if table exists
    if '<table' in content and '.table-responsive {' not in content:
        if '</style>' in content:
            table_css = """
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
    """
            content = content.replace('</style>', table_css + '</style>')

    # 4. Wrap tables in <div class="table-responsive"> if not already wrapped
    if '<table' in content:
        import re
        # Find all tables
        tables = re.findall(r'(<table.*?</table>)', content, re.DOTALL)
        for t in tables:
            # Check if it's already wrapped (simple check: if preceded by <div class="table-responsive"> in the same document... actually just regex replace the table)
            # A safer way:
            if '<div class="table-responsive">\n        <table' not in content and '<div class="table-responsive">\n            <table' not in content:
                content = content.replace(t, f'<div class="table-responsive">\n{t}\n</div>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

templates = glob.glob('d:/Work/new_msg/templates/*.html')
for t in templates:
    if 'react_' not in t:
        patch_file(t)

print("Systematic responsive CSS applied to all Django templates.")
