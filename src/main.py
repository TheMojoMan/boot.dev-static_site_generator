#from textnode import TextType, TextNode
from htmlnode import HTMLNode
from markdown_converter import markdown_to_html_node, extract_title

import os
import shutil

def copy_files(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for filename in os.listdir(source):
        path_from = os.path.join(source, filename)
        path_to = os.path.join(dest, filename)
        print(f"Copying {path_from} to {path_to}")
        if os.path.isdir(path_from):
            copy_files(path_from, path_to)
        else:
            shutil.copy(path_from, path_to)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise Exception(f"{from_path} does not exist.")
    if not os.path.exists(template_path):
        raise Exception(f"{template_path} does not exist.")

    with open(from_path, 'r') as file:
        md = file.read()
    with open(template_path, 'r') as file:
        template_str = file.read()

    html_node = markdown_to_html_node(md)
    html_str = html_node.to_html()
    title = extract_title(md)
    template_str = template_str.replace("{{ Title }}", title)
    template_str = template_str.replace("{{ Content }}", html_str)

    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    with open(dest_path, 'w') as file:
        file.write(template_str)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dir_path_content):
        raise Exception(f"{dir_path_content} does not exist.")
    if not os.path.exists(template_path):
        raise Exception(f"{template_path} does not exist.")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
            
    for filename in os.listdir(dir_path_content):
        path_from = os.path.join(dir_path_content, filename)
        path_to = os.path.join(dest_dir_path, filename)
        print(f"Copying {path_from} to {path_to}")
        if os.path.isfile(path_from):
            generate_page(path_from, template_path, path_to.replace(".md", ".html"))
        else:
            generate_pages_recursive(path_from, template_path, path_to)


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
