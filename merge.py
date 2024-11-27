import random
import os

def format_html(html_code):
    # Simple HTML formatting by adding indentation
    lines = html_code.splitlines()
    formatted_lines = []
    indent_level = 0
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith("</"):
            indent_level -= 1
        formatted_lines.append("    " * indent_level + stripped_line)
        if not stripped_line.startswith("</") and not stripped_line.endswith("/>") and stripped_line.endswith(">"):
            indent_level += 1
    return "\n".join(formatted_lines)

def count_folders(directory):
    folder_list = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    return len(folder_list)

def parse_tag(path, tag):
    with open(path, "r") as path_content:
        content = path_content.read()
        tag_start = f"<{tag}>"
        tag_end = f"</{tag}>"
        
        start_index = content.find(tag_start)
        end_index = content.find(tag_end)
        
        if start_index != -1 and end_index != -1:
            return content[start_index:end_index + len(tag_end)]
        else:
            print(f"No <{tag}> tag found in {path}")
            return ""

def merge_html_files(header_file_path, body_file_path):
    html_body = parse_tag(header_file_path, "body") + parse_tag(body_file_path, "body")
    #print("HTML BODY: ", html_body)
    html_style = parse_tag(header_file_path, "style") + parse_tag(body_file_path, "style")
    #print("HTML STYLE: ", html_style)
    print("merging")
    
    html_page = format_html(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {html_style}
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """)
    
    if "None" in html_page:
        print("Error occurred. Element not found")
    
    with open("output.html", "w") as file:
        file.write(html_page)

header_path_number = random.randint(1, count_folders("Header"))
body_path_number = random.randint(1, count_folders("Body"))
print(str(count_folders("Header")) + " ~~ Amount of Headers")
print(str(count_folders("Body")) + " ~~ Amount of Body's")
print(header_path_number , "<~ Header num")
print(body_path_number , "<~ Body num")

header_path = f'./Header/ex{header_path_number}/index.html'
body_path = f'./Body/ex{body_path_number}/index.html'

merge_html_files(header_path, body_path)
