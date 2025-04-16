import os
import shutil
import sys

from markdown_parser import markdown_to_html_node, extract_title

def copy_static_files(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    files = os.listdir(source_dir)
    for item in os.listdir(source_dir):
        source_item_path = os.path.join(source_dir, item)
        dest_item_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_item_path):
            print(f"Copying file: {source_item_path} to {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        else:
            print(f"Creating directory: {dest_item_path}")
            os.mkdir(dest_item_path)
            copy_static_files(source_item_path, dest_item_path)

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        content = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    
    html_node = markdown_to_html_node(content)
    html = html_node.to_html()

    title = extract_title(content)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    html = html.replace('href="/', f'href="{base_path}')
    html = html.replace('src="/', f'src="{base_path}')

    dirs = dest_path.split("/")
    for i in range(len(dirs)-1):
        path = "/".join(dirs[:i+1])
        if not os.path.exists(path):
            os.makedirs(path)

    with open(dest_path, 'w') as f:
        f.write(html)

def generate_pages_recursively(from_path, template_path, dest_path, base_path):
    if os.path.isfile(from_path) and from_path.endswith('.md'):
        dest_file_path = dest_path.replace('.md', '.html')
        generate_page(from_path, template_path, dest_file_path, base_path)
    elif os.path.isdir(from_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        for item in os.listdir(from_path):
            source_item_path = os.path.join(from_path, item)
            dest_item_path = os.path.join(dest_path, item)
            generate_pages_recursively(source_item_path, template_path, dest_item_path, base_path)



if __name__ == "__main__":
    source_dir = "static"
    dest_dir = "docs/static"

    basepath = "/"

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    copy_static_files(source_dir, dest_dir)

    generate_pages_recursively(
        from_path="content/",
        template_path="template.html",
        dest_path="docs",
        base_path=basepath)